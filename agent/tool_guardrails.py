"""Pure tool-call loop guardrail primitives.

The controller in this module is intentionally side-effect free: it tracks
per-turn tool-call observations and returns decisions. Runtime code owns whether
those decisions become warning guidance, synthetic tool results, or controlled
turn halts.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Mapping

from utils import safe_json_loads
from agent.tool_result_classification import file_mutation_result_landed


IDEMPOTENT_TOOL_NAMES = frozenset(
    {
        "read_file",
        "search_files",
        "web_search",
        "web_extract",
        "session_search",
        "skill_view",
        "skills_list",
        "browser_snapshot",
        "browser_console",
        "browser_get_images",
        "mcp_filesystem_read_file",
        "mcp_filesystem_read_text_file",
        "mcp_filesystem_read_multiple_files",
        "mcp_filesystem_list_directory",
        "mcp_filesystem_list_directory_with_sizes",
        "mcp_filesystem_directory_tree",
        "mcp_filesystem_get_file_info",
        "mcp_filesystem_search_files",
    }
)

MUTATING_TOOL_NAMES = frozenset(
    {
        "terminal",
        "execute_code",
        "write_file",
        "patch",
        "todo_list",
        "memory",
        "skill_manage",
        "browser_click",
        "browser_type",
        "browser_press",
        "browser_scroll",
        "browser_navigate",
        "send_message",
        "cronjob_manage",
        "delegate_task",
        "process_manage",
    }
)

# Tools that are legitimately re-invoked with identical arguments and may
# legitimately return an unchanged result while waiting on external progress —
# background-process management and job pollers. The identical-call loop
# notice (agent.stall_guards) never fires for these, so polling patterns like
# ``process(action="poll")`` or repeatedly checking a generation job stay
# unannotated.
STALL_GUARD_REPEATABLE_TOOLS = frozenset(
    {
        "process_manage",
    }
)

# Poller naming conventions (e.g. ``<vendor>_get_result``) used by generated /
# MCP tool surfaces. Matched as suffixes so vendor-prefixed pollers are exempt
# without enumerating every vendor.
_STALL_GUARD_REPEATABLE_SUFFIXES = (
    "_get_result",
    "_poll",
)

# The notice fires on the Nth consecutive identical call (same tool, same
# canonical args, same result). 3 tolerates one legitimate double-check while
# catching the observed re-issue loops (3x/4x identical calls in eval traces).
STALL_GUARD_IDENTICAL_CALL_THRESHOLD = 3

# Result-reference stubbing (agent.stall_guards): from the 2nd consecutive
# identical call whose FRESH result is byte-identical to the previous one,
# the duplicate payload is replaced in context by a short reference stub.
# Results under this size aren't worth stubbing (the stub itself plus the
# lost locality outweigh the savings), and error results are never stubbed
# (the model must see every fresh error verbatim).
IDENTICAL_RESULT_STUB_MIN_CHARS = 512

# How much of the canonical args JSON the stub carries so the model still
# knows WHAT the referenced call was even if context compression later
# evicts the referenced result (cheap dangling-reference mitigation).
_RESULT_STUB_ARGS_PREVIEW_CHARS = 120


# Tools whose "failure" is a normal, informative outcome of legitimate work:
# a red test run, a grep with no matches, a failing build during a fix loop, a
# page that times out. Hard stops never fire on these from failure counts of
# DIFFERENT commands (same_tool_failure) — only an exact-args replay with NO
# intervening change, or an identical-result streak, can halt them.
FAILURE_TOLERANT_TOOL_NAMES = frozenset(
    {
        "terminal",
        "execute_code",
        "process_manage",
        "process",
        "browser_navigate",
        "web_extract",
    }
)

# A landed mutation between two attempts means the retry is a NEW experiment
# (edit -> re-run) rather than a replay. A successful call to one of these
# marks progress for every failing signature still being counted this turn.
PROGRESS_RESET_TOOL_NAMES = frozenset(
    {
        "write_file",
        "patch",
        "terminal",
        "execute_code",
        "browser_click",
        "browser_type",
        "browser_press",
        "browser_navigate",
        "process_manage",
        "process",
        "delegate_task",
        "send_message",
        "cronjob",
        "cronjob_manage",
        "todo",
        "todo_list",
        "memory",
        "skill_manage",
    }
)


def is_stall_guard_repeatable(tool_name: str) -> bool:
    """Whether a tool is exempt from the identical-call loop notice."""
    if tool_name in STALL_GUARD_REPEATABLE_TOOLS:
        return True
    return tool_name.endswith(_STALL_GUARD_REPEATABLE_SUFFIXES)


@dataclass(frozen=True)
class ToolCallGuardrailConfig:
    """Thresholds for per-turn tool-call loop detection.

    Warnings are enabled by default and never prevent tool execution. Hard stops
    stay opt-in for interactive CLI/TUI/Desktop/ACP sessions, but default on for
    non-interactive gateway/cron platforms where nobody is present to interrupt
    a model that ignores loop warnings.
    """

    warnings_enabled: bool = True
    hard_stop_enabled: bool = False
    non_interactive_hard_stop_enabled: bool = True
    exact_failure_warn_after: int = 2
    exact_failure_block_after: int = 5
    same_tool_failure_warn_after: int = 3
    same_tool_failure_halt_after: int = 8
    no_progress_warn_after: int = 2
    no_progress_block_after: int = 5
    idempotent_tools: frozenset[str] = field(default_factory=lambda: IDEMPOTENT_TOOL_NAMES)
    mutating_tools: frozenset[str] = field(default_factory=lambda: MUTATING_TOOL_NAMES)
    loop_caps: "LoopCapConfig" = field(default_factory=lambda: LoopCapConfig())

    @classmethod
    def from_mapping(
        cls,
        data: Mapping[str, Any] | None,
        *,
        platform: str | None = None,
    ) -> "ToolCallGuardrailConfig":
        """Build config from the `tool_loop_guardrails` config.yaml section."""
        if not isinstance(data, Mapping):
            data = {}

        warn_after = data.get("warn_after")
        if not isinstance(warn_after, Mapping):
            warn_after = {}
        hard_stop_after = data.get("hard_stop_after")
        if not isinstance(hard_stop_after, Mapping):
            hard_stop_after = {}

        defaults = cls()
        hard_stop_enabled = _as_bool(data.get("hard_stop_enabled"), defaults.hard_stop_enabled)
        non_interactive_hard_stop_enabled = _as_bool(
            data.get("non_interactive_hard_stop_enabled"),
            defaults.non_interactive_hard_stop_enabled,
        )
        if _is_non_interactive_platform(platform) and non_interactive_hard_stop_enabled:
            hard_stop_enabled = True

        return cls(
            warnings_enabled=_as_bool(data.get("warnings_enabled"), defaults.warnings_enabled),
            hard_stop_enabled=hard_stop_enabled,
            non_interactive_hard_stop_enabled=non_interactive_hard_stop_enabled,
            exact_failure_warn_after=_positive_int(
                warn_after.get("exact_failure", data.get("exact_failure_warn_after")),
                defaults.exact_failure_warn_after,
            ),
            same_tool_failure_warn_after=_positive_int(
                warn_after.get("same_tool_failure", data.get("same_tool_failure_warn_after")),
                defaults.same_tool_failure_warn_after,
            ),
            no_progress_warn_after=_positive_int(
                warn_after.get("idempotent_no_progress", data.get("no_progress_warn_after")),
                defaults.no_progress_warn_after,
            ),
            exact_failure_block_after=_positive_int(
                hard_stop_after.get("exact_failure", data.get("exact_failure_block_after")),
                defaults.exact_failure_block_after,
            ),
            same_tool_failure_halt_after=_positive_int(
                hard_stop_after.get("same_tool_failure", data.get("same_tool_failure_halt_after")),
                defaults.same_tool_failure_halt_after,
            ),
            no_progress_block_after=_positive_int(
                hard_stop_after.get("idempotent_no_progress", data.get("no_progress_block_after")),
                defaults.no_progress_block_after,
            ),
            loop_caps=LoopCapConfig.from_mapping(data.get("loop_caps")),
        )


# Default session-wide caps, matching Claude Code's v2.1.212 runaway-loop
# Per-turn (per-agent-loop) caps on runaway-prone tool calls. Counts reset at
# the start of every agent loop (reset_for_turn), so the limit is "within a
# single turn" rather than cumulative over the whole session. A single loop
# issuing dozens of web searches or spawning dozens of subagents is already
# pathological, so the defaults are deliberately low.
_DEFAULT_MAX_WEB_SEARCHES_PER_TURN = 50
_DEFAULT_MAX_SUBAGENTS_PER_TURN = 50


@dataclass(frozen=True)
class LoopCapConfig:
    """Per-turn caps on runaway-prone tool calls.

    Inspired by Claude Code v2.1.212 (Week 29, July 2026), which added caps on
    WebSearch calls and subagent spawns to stop runaway search / delegation
    loops. Here the caps count *within a single agent loop* (one turn): the
    counters reset in ``reset_for_turn`` at the start of every
    ``run_conversation``, so a legitimate multi-turn session is never starved,
    but a single turn that spirals into an unbounded search / delegation loop
    is stopped.

    Semantics differ from the per-turn loop *detector* above (which keys on
    repeated identical/failing calls): these caps are a hard ceiling on the
    total count of a tool within the turn and fire regardless of
    ``hard_stop_enabled``. A value of ``0`` disables the cap (unlimited).
    """

    max_web_searches: int = _DEFAULT_MAX_WEB_SEARCHES_PER_TURN
    max_subagents: int = _DEFAULT_MAX_SUBAGENTS_PER_TURN

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "LoopCapConfig":
        """Build config from the ``tool_loop_guardrails.loop_caps`` section."""
        if not isinstance(data, Mapping):
            return cls()
        defaults = cls()
        return cls(
            max_web_searches=_non_negative_int(
                data.get("max_web_searches"), defaults.max_web_searches
            ),
            max_subagents=_non_negative_int(
                data.get("max_subagents"), defaults.max_subagents
            ),
        )


_INTERACTIVE_PLATFORMS = frozenset({"cli", "tui", "desktop", "acp"})

# Platforms that are not chat gateways but whose work is a bounded, supervised
# task loop: a subagent inherits its parent's budget and is stopped by the
# parent; api_server runs have a live client holding the request. Both do
# real edit -> re-run work, so they keep the interactive (warn-only) default.
_SUPERVISED_TASK_PLATFORMS = frozenset({"subagent", "api_server"})


def _is_non_interactive_platform(platform: str | None) -> bool:
    """Return true for gateway/cron sessions where tool loops are unattended."""
    if not isinstance(platform, str) or not platform.strip():
        return False
    key = platform.strip().lower()
    if key in _INTERACTIVE_PLATFORMS or key in _SUPERVISED_TASK_PLATFORMS:
        return False
    return True


@dataclass(frozen=True)
class IdenticalCallObservation:
    """Outcome of observing one completed tool call for the stall guards.

    ``notice`` is the identical-call loop-breaker notice (appended after the
    result). ``stub`` is the result-reference replacement for a byte-identical
    duplicate result (replaces the result content). Both may be set on the
    same call (3rd+ identical call): the stub replaces the payload and the
    notice is appended after it.
    """

    notice: str | None = None
    stub: str | None = None


@dataclass(frozen=True)
class ToolCallSignature:
    """Stable, non-reversible identity for a tool name plus canonical args."""

    tool_name: str
    args_hash: str

    @classmethod
    def from_call(cls, tool_name: str, args: Mapping[str, Any] | None) -> "ToolCallSignature":
        canonical = canonical_tool_args(args or {})
        return cls(tool_name=tool_name, args_hash=_sha256(canonical))

    def to_metadata(self) -> dict[str, str]:
        """Return public metadata without raw argument values."""
        return {"tool_name": self.tool_name, "args_hash": self.args_hash}


@dataclass(frozen=True)
class ToolGuardrailDecision:
    """Decision returned by the tool-call guardrail controller."""

    action: str = "allow"  # allow | warn | block | halt
    code: str = "allow"
    message: str = ""
    tool_name: str = ""
    count: int = 0
    signature: ToolCallSignature | None = None

    @property
    def allows_execution(self) -> bool:
        return self.action in {"allow", "warn"}

    @property
    def should_halt(self) -> bool:
        return self.action in {"block", "halt"}

    def to_metadata(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "action": self.action,
            "code": self.code,
            "message": self.message,
            "tool_name": self.tool_name,
            "count": self.count,
        }
        if self.signature is not None:
            data["signature"] = self.signature.to_metadata()
        return data


def canonical_tool_args(args: Mapping[str, Any]) -> str:
    """Return sorted compact JSON for parsed tool arguments."""
    if not isinstance(args, Mapping):
        raise TypeError(f"tool args must be a mapping, got {type(args).__name__}")
    return json.dumps(
        args,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def classify_tool_failure(tool_name: str, result: str | None) -> tuple[bool, str]:
    """Safety-fallback classifier used only when callers don't pass ``failed``.

    Mirrors ``agent.display._detect_tool_failure`` exactly so the guardrail
    never disagrees with the CLI's user-visible ``[error]`` tag. Production
    callers in ``run_agent.py`` always pass an explicit ``failed=`` derived
    from ``_detect_tool_failure``; this function exists so standalone callers
    (tests, tooling) still get consistent behavior.
    """
    if result is None:
        return False, ""
    if file_mutation_result_landed(tool_name, result):
        return False, ""

    if tool_name == "terminal":
        data = safe_json_loads(result)
        if isinstance(data, dict):
            exit_code = data.get("exit_code")
            if exit_code is not None and exit_code != 0:
                return True, f" [exit {exit_code}]"
        return False, ""

    if tool_name == "memory":
        data = safe_json_loads(result)
        if isinstance(data, dict):
            if data.get("success") is False and "exceed the limit" in data.get("error", ""):
                return True, " [full]"

    lower = result[:500].lower()
    if '"error"' in lower or '"failed"' in lower or result.startswith("Error"):
        return True, " [error]"

    return False, ""


class ToolCallGuardrailController:
    """Per-turn controller for repeated failed/non-progressing tool calls."""

    def __init__(self, config: ToolCallGuardrailConfig | None = None):
        self.config = config or ToolCallGuardrailConfig()
        self.reset_for_turn()

    def reset_for_turn(self) -> None:
        self._exact_failure_counts: dict[ToolCallSignature, int] = {}
        self._same_tool_failure_counts: dict[str, int] = {}
        # signature -> a mutating call succeeded since its last failure
        self._progress_since_failure: dict[ToolCallSignature, bool] = {}
        self._no_progress: dict[ToolCallSignature, tuple[str, int]] = {}
        self._halt_decision: ToolGuardrailDecision | None = None
        # Identical-call loop-breaker state (agent.stall_guards): tracks the
        # CONSECUTIVE streak of identical (tool, canonical args) calls whose
        # results were also identical. Any different call — or a different
        # result — resets the streak, so legitimate re-reads after edits and
        # varied polling are never flagged. Per-turn, like everything else here.
        # NOTE: open PR #85352 (patrykkopycinski) tracks no-progress loops
        # ACROSS turns via a detection window — a different mechanism from
        # this per-turn consecutive streak. Coordinate future work there.
        self._identical_streak_sig: ToolCallSignature | None = None
        self._identical_streak_result_hash: str = ""
        self._identical_streak_count: int = 0
        # tool_call_id of the FIRST call in the current streak, so a
        # result-reference stub can point at the message that carries the
        # full payload.
        self._identical_streak_first_call_id: str = ""
        # tool_call_id -> spillover file path for results that were persisted
        # out of context (persisted-output preview). Lets a reference stub
        # carry the file path so the reference can't dangle when the first
        # occurrence entered context as a preview.
        self._persisted_result_paths: dict[str, str] = {}
        # Per-turn runaway-loop cap counters. Reset every turn (this method
        # runs at the start of each run_conversation), so the caps bound a
        # single agent loop rather than accumulating across the session.
        self._turn_web_search_count = 0
        self._turn_subagent_count = 0

    @property
    def halt_decision(self) -> ToolGuardrailDecision | None:
        return self._halt_decision

    def before_call(self, tool_name: str, args: Mapping[str, Any] | None) -> ToolGuardrailDecision:
        signature = ToolCallSignature.from_call(tool_name, _coerce_args(args))

        # ── Per-turn runaway-loop caps ──────────────────────────────────
        # These are hard ceilings on how many times a runaway-prone tool may
        # be called within a single agent loop (turn). They apply regardless
        # of hard_stop_enabled (which only governs the per-turn loop detector).
        # We block BEFORE the call runs once the count is already at the cap,
        # then increment for an allowed call so the (cap+1)-th is refused.
        cap_block = self._check_loop_cap(tool_name, _coerce_args(args), signature)
        if cap_block is not None:
            return cap_block

        if not self.config.hard_stop_enabled:
            return ToolGuardrailDecision(tool_name=tool_name, signature=signature)

        exact_count = self._exact_failure_counts.get(signature, 0)
        if self._progress_since_failure.get(signature):
            # Something landed since this call last failed — let it run; the
            # streak restarts in after_call if it fails again.
            exact_count = 0
        if exact_count >= self.config.exact_failure_block_after:
            decision = ToolGuardrailDecision(
                action="block",
                code="repeated_exact_failure_block",
                message=(
                    f"Blocked {tool_name}: the same tool call failed {exact_count} "
                    "times with identical arguments. Stop retrying it unchanged; "
                    "change strategy or explain the blocker."
                ),
                tool_name=tool_name,
                count=exact_count,
                signature=signature,
            )
            self._halt_decision = decision
            return decision

        if self._is_idempotent(tool_name):
            record = self._no_progress.get(signature)
            if record is not None:
                _result_hash, repeat_count = record
                if repeat_count >= self.config.no_progress_block_after:
                    decision = ToolGuardrailDecision(
                        action="block",
                        code="idempotent_no_progress_block",
                        message=(
                            f"Blocked {tool_name}: this read-only call returned the same "
                            f"result {repeat_count} times. Stop repeating it unchanged; "
                            "use the result already provided or try a different query."
                        ),
                        tool_name=tool_name,
                        count=repeat_count,
                        signature=signature,
                    )
                    self._halt_decision = decision
                    return decision

        return ToolGuardrailDecision(tool_name=tool_name, signature=signature)

    def after_call(
        self,
        tool_name: str,
        args: Mapping[str, Any] | None,
        result: str | None,
        *,
        failed: bool | None = None,
    ) -> ToolGuardrailDecision:
        args = _coerce_args(args)
        signature = ToolCallSignature.from_call(tool_name, args)
        if failed is None:
            failed, _ = classify_tool_failure(tool_name, result)

        if failed:
            # An identical failing call is only a REPLAY if nothing landed in
            # between. If any mutating call succeeded since the previous
            # identical failure (edit -> re-run pytest, click -> re-snapshot),
            # the retry is a new experiment: restart the exact-args streak.
            if self._progress_since_failure.pop(signature, False):
                self._exact_failure_counts.pop(signature, None)
            exact_count = self._exact_failure_counts.get(signature, 0) + 1
            self._exact_failure_counts[signature] = exact_count
            self._no_progress.pop(signature, None)

            same_count = self._same_tool_failure_counts.get(tool_name, 0) + 1
            self._same_tool_failure_counts[tool_name] = same_count

            # same_tool_failure counts DIFFERENT args on one tool. For tools
            # whose non-zero exit is ordinary work output (terminal,
            # execute_code, pollers) a run of distinct red commands is
            # diagnosis, not a loop — warn, never halt. The exact-args replay
            # path still applies to them.
            same_tool_halt_eligible = tool_name not in FAILURE_TOLERANT_TOOL_NAMES
            if (
                self.config.hard_stop_enabled
                and same_tool_halt_eligible
                and same_count >= self.config.same_tool_failure_halt_after
            ):
                decision = ToolGuardrailDecision(
                    action="halt",
                    code="same_tool_failure_halt",
                    message=(
                        f"Stopped {tool_name}: it failed {same_count} times this turn. "
                        "Stop retrying the same failing tool path and choose a different approach."
                    ),
                    tool_name=tool_name,
                    count=same_count,
                    signature=signature,
                )
                self._halt_decision = decision
                return decision

            if self.config.warnings_enabled and exact_count >= self.config.exact_failure_warn_after:
                return ToolGuardrailDecision(
                    action="warn",
                    code="repeated_exact_failure_warning",
                    message=(
                        f"{tool_name} has failed {exact_count} times with identical arguments. "
                        "This looks like a loop; inspect the error and change strategy "
                        "instead of retrying it unchanged."
                    ),
                    tool_name=tool_name,
                    count=exact_count,
                    signature=signature,
                )

            if self.config.warnings_enabled and same_count >= self.config.same_tool_failure_warn_after:
                return ToolGuardrailDecision(
                    action="warn",
                    code="same_tool_failure_warning",
                    message=_tool_failure_recovery_hint(tool_name, same_count),
                    tool_name=tool_name,
                    count=same_count,
                    signature=signature,
                )

            return ToolGuardrailDecision(tool_name=tool_name, count=exact_count, signature=signature)

        self._exact_failure_counts.pop(signature, None)
        self._same_tool_failure_counts.pop(tool_name, None)

        # A successful mutation is progress for every failing signature still
        # being counted this turn: the next identical retry runs against
        # changed state, so it is a fresh attempt rather than a replay. Pure
        # loops never mutate anything between attempts, so the replay detector
        # keeps its teeth.
        if tool_name in PROGRESS_RESET_TOOL_NAMES or file_mutation_result_landed(tool_name, result):
            for sig in list(self._exact_failure_counts):
                self._progress_since_failure[sig] = True
            self._same_tool_failure_counts.clear()

        if not self._is_idempotent(tool_name):
            self._no_progress.pop(signature, None)
            return ToolGuardrailDecision(tool_name=tool_name, signature=signature)

        result_hash = _result_hash(result)
        previous = self._no_progress.get(signature)
        repeat_count = 1
        if previous is not None and previous[0] == result_hash:
            repeat_count = previous[1] + 1
        self._no_progress[signature] = (result_hash, repeat_count)

        if self.config.warnings_enabled and repeat_count >= self.config.no_progress_warn_after:
            return ToolGuardrailDecision(
                action="warn",
                code="idempotent_no_progress_warning",
                message=(
                    f"{tool_name} returned the same result {repeat_count} times. "
                    "Use the result already provided or change the query instead of "
                    "repeating it unchanged."
                ),
                tool_name=tool_name,
                count=repeat_count,
                signature=signature,
            )

        return ToolGuardrailDecision(tool_name=tool_name, count=repeat_count, signature=signature)

    def _is_idempotent(self, tool_name: str) -> bool:
        if tool_name in self.config.mutating_tools:
            return False
        return tool_name in self.config.idempotent_tools

    def observe_identical_call(
        self,
        tool_name: str,
        args: Mapping[str, Any] | None,
        result: str | None,
    ) -> str | None:
        """Track consecutive identical calls; return a loop-breaker notice or None.

        Back-compat wrapper around :meth:`observe_call` for callers that only
        care about the loop-breaker notice.
        """
        return self.observe_call(tool_name, args, result).notice

    def observe_call(
        self,
        tool_name: str,
        args: Mapping[str, Any] | None,
        result: str | None,
        *,
        tool_call_id: str = "",
        failed: bool = False,
    ) -> "IdenticalCallObservation":
        """Track consecutive identical calls; return notice + dedupe stub info.

        Two independent outputs from the same consecutive-streak tracker:

        - ``notice``: the compact loop-breaker notice, fired when the SAME
          tool is called with identical canonical arguments AND returns an
          identical result for the ``STALL_GUARD_IDENTICAL_CALL_THRESHOLD``-th
          (and every subsequent) consecutive time within the turn. Purely
          observational — never blocks the call. Allowlisted pollers
          (``is_stall_guard_repeatable``) are exempt from the NOTICE.
        - ``stub``: a short reference replacement for the CURRENT result,
          produced from the 2nd consecutive identical call whose fresh result
          is byte-identical to the previous one. The tool still executed —
          only the context representation is deduplicated, so polling
          semantics are preserved (a changed result flows through whole and
          resets the streak). Pollers are NOT exempt from stubbing: for a
          poller, an identical result means nothing changed, which is exactly
          when the stub saves the most context and loses nothing. Results
          under ``IDENTICAL_RESULT_STUB_MIN_CHARS`` and failed/error results
          are never stubbed, and only plain-string results are considered.

        Any intervening different call or changed result resets the streak.
        Callers substitute/append at tool RESULT construction time, which is
        cache-safe: tool results are append-only and never mutate
        already-sent context.
        """
        is_plain_str = isinstance(result, str)
        signature = ToolCallSignature.from_call(tool_name, _coerce_args(args))
        result_hash = _result_hash(result) if is_plain_str else ""

        if (
            is_plain_str
            and self._identical_streak_sig == signature
            and self._identical_streak_result_hash == result_hash
        ):
            self._identical_streak_count += 1
        else:
            # New streak (or non-string result, which never forms a streak —
            # multimodal content lists pass through untouched).
            self._identical_streak_sig = signature if is_plain_str else None
            self._identical_streak_result_hash = result_hash
            self._identical_streak_count = 1 if is_plain_str else 0
            self._identical_streak_first_call_id = tool_call_id or ""

        count = self._identical_streak_count

        notice = None
        if (
            not is_stall_guard_repeatable(tool_name)
            and count >= STALL_GUARD_IDENTICAL_CALL_THRESHOLD
        ):
            ordinal = f"{count}{'th' if 11 <= count % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(count % 10, 'th')}"
            notice = (
                f"[hermes note: this is the {ordinal} consecutive identical call to "
                f"{tool_name} with identical arguments returning the same result. "
                "Do not repeat it — change arguments, use a different tool, or "
                "proceed with what you have.]"
            )
            # Hard-stop widening (#89069 / #100849 bundle): the per-turn
            # no-progress BLOCK above only covers tools in idempotent_tools, so
            # a model replaying the same successful `terminal`/`skill_view`
            # call with a byte-identical result ran until the iteration budget.
            # The consecutive-identical streak is tool-agnostic; when hard
            # stops are enabled, halt at the same idempotent_no_progress
            # threshold. Pollers stay exempt (an unchanged poll is progress).
            if (
                self.config.hard_stop_enabled
                and count >= self.config.no_progress_block_after
                and self._halt_decision is None
            ):
                self._halt_decision = ToolGuardrailDecision(
                    action="halt",
                    code="identical_call_streak_halt",
                    message=(
                        f"Stopped {tool_name}: the same call with identical arguments "
                        f"returned the same result {count} times in a row. Stop "
                        "repeating it unchanged; use the result already provided or "
                        "change strategy."
                    ),
                    tool_name=tool_name,
                    count=count,
                    signature=signature,
                )

        stub = None
        if (
            is_plain_str
            and count >= 2
            and not failed
            and len(result) >= IDENTICAL_RESULT_STUB_MIN_CHARS
        ):
            stub = self._build_result_reference_stub(tool_name, args)

        return IdenticalCallObservation(notice=notice, stub=stub)

    def record_persisted_result(self, tool_call_id: str, file_path: str) -> None:
        """Remember the spillover path a persisted result was saved to.

        When the first occurrence of a result entered context as a
        persisted-output preview, a later reference stub must carry the
        spillover file path so the reference can't dangle.
        """
        if tool_call_id and file_path:
            self._persisted_result_paths[tool_call_id] = file_path

    def _build_result_reference_stub(
        self, tool_name: str, args: Mapping[str, Any] | None
    ) -> str:
        """Build the reference stub replacing a byte-identical duplicate result.

        Carries the tool name + a canonical-args preview so that even if
        context compression later evicts the referenced result, the model
        still knows WHAT the call was (cheap dangling-reference mitigation).
        """
        try:
            args_preview = canonical_tool_args(_coerce_args(args))
        except TypeError:
            args_preview = "{}"
        if len(args_preview) > _RESULT_STUB_ARGS_PREVIEW_CHARS:
            args_preview = args_preview[:_RESULT_STUB_ARGS_PREVIEW_CHARS] + "…"
        first_id = self._identical_streak_first_call_id
        ref = f" (tool_call_id {first_id})" if first_id else ""
        stub = (
            f"[hermes note: this result is byte-identical to the {tool_name} "
            f"result earlier this turn{ref}. Refer to that result; it has not "
            f"changed. Args: {args_preview}]"
        )
        spill_path = self._persisted_result_paths.get(first_id) if first_id else None
        if spill_path:
            stub += (
                f"\n[The referenced result was persisted to: {spill_path} — "
                "page through it with read_file if you need the full content.]"
            )
        return stub

    def _check_loop_cap(
        self,
        tool_name: str,
        args: Mapping[str, Any],
        signature: ToolCallSignature,
    ) -> ToolGuardrailDecision | None:
        """Enforce and advance the per-turn runaway-loop counters.

        Returns a ``block`` decision when the cap is already reached, otherwise
        increments the relevant counter for the allowed call and returns
        ``None``. A cap of 0 disables that limit entirely. Counters reset each
        turn via ``reset_for_turn``.
        """
        caps = self.config.loop_caps

        if tool_name == "web_search":
            cap = caps.max_web_searches
            if cap and self._turn_web_search_count >= cap:
                decision = ToolGuardrailDecision(
                    action="block",
                    code="loop_web_search_cap",
                    message=(
                        f"Blocked web_search: this turn has already made {cap} "
                        "web searches, the per-turn limit. This looks like a "
                        "runaway search loop. Work with the results you already "
                        "have and give the user your answer."
                    ),
                    tool_name=tool_name,
                    count=self._turn_web_search_count,
                    signature=signature,
                )
                self._halt_decision = decision
                return decision
            self._turn_web_search_count += 1
            return None

        if tool_name == "delegate_task":
            cap = caps.max_subagents
            if not cap:
                return None
            spawn_count = _subagent_spawn_count(args)
            if spawn_count == 0:
                # Control action (list/steer/stop) — spawns nothing. Never
                # block: once the spawn cap is hit, steering/stopping the
                # existing children is exactly what should still work.
                return None
            if self._turn_subagent_count >= cap:
                decision = ToolGuardrailDecision(
                    action="block",
                    code="loop_subagent_cap",
                    message=(
                        f"Blocked delegate_task: this turn has already spawned "
                        f"{self._turn_subagent_count} subagents (limit {cap}). "
                        "This looks like a runaway delegation loop. Finish the "
                        "work with the results you have and answer the user."
                    ),
                    tool_name=tool_name,
                    count=self._turn_subagent_count,
                    signature=signature,
                )
                self._halt_decision = decision
                return decision
            self._turn_subagent_count += spawn_count
            return None

        return None


def toolguard_synthetic_result(decision: ToolGuardrailDecision) -> str:
    """Build a synthetic role=tool content string for a blocked tool call."""
    return json.dumps(
        {
            "error": decision.message,
            "guardrail": decision.to_metadata(),
        },
        ensure_ascii=False,
    )


def append_toolguard_guidance(result: str, decision: ToolGuardrailDecision) -> str:
    """Append runtime guidance to the current tool result content."""
    if decision.action not in {"warn", "halt"} or not decision.message:
        return result
    label = "Tool loop hard stop" if decision.action == "halt" else "Tool loop warning"
    suffix = (
        f"\n\n[{label}: "
        f"{decision.code}; count={decision.count}; {decision.message}]"
    )
    return (result or "") + suffix


def _tool_failure_recovery_hint(tool_name: str, count: int) -> str:
    """Action-oriented guidance for recovering from repeated tool failures."""
    common = (
        f"{tool_name} has failed {count} times this turn. This looks like a loop. "
        "Do not switch to text-only replies; keep using tools, but diagnose before retrying. "
        "First inspect the latest error/output and verify your assumptions. "
    )
    if tool_name == "terminal":
        return common + (
            "For terminal failures, run a small diagnostic such as `pwd && ls -la` "
            "in the same tool, then try an absolute path, a simpler command, a different "
            "working directory, or a different tool such as read_file/write_file/patch."
        )
    return common + (
        "Try different arguments, a narrower query/path, an absolute path when relevant, "
        "or a different tool that can make progress. If the blocker is external, report "
        "the blocker after one diagnostic attempt instead of repeating the same failing path."
    )


def _coerce_args(args: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return args if isinstance(args, Mapping) else {}


def _result_hash(result: str | None) -> str:
    parsed = safe_json_loads(result or "")
    if parsed is not None:
        try:
            canonical = json.dumps(
                parsed,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            )
        except TypeError:
            canonical = str(parsed)
    else:
        canonical = result or ""
    return _sha256(canonical)


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on", "enabled"}:
            return True
        if lowered in {"0", "false", "no", "off", "disabled"}:
            return False
    return default


def _positive_int(value: Any, default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 1 else default


def _non_negative_int(value: Any, default: int) -> int:
    """Parse a session-cap value. 0 is a valid (disable) value; negatives and
    junk fall back to the default."""
    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _subagent_spawn_count(args: Mapping[str, Any]) -> int:
    """How many subagents a single delegate_task call spawns.

    delegate_task runs in one of two modes: a batch (``tasks`` is a non-empty
    list, one child per item) or a single task (``goal``). Count the batch size
    when present, otherwise 1, so the session subagent cap reflects real spawns
    rather than delegate_task invocations. Control actions (list/steer/stop)
    spawn nothing and must not consume the cap.
    """
    if isinstance(args, Mapping):
        action = str(args.get("action") or "").strip().lower()
        if action in ("list", "steer", "stop"):
            return 0
    tasks = args.get("tasks") if isinstance(args, Mapping) else None
    if isinstance(tasks, list) and tasks:
        return len(tasks)
    return 1


def _sha256(value: str) -> str:
    # surrogatepass: tool results scraped from the web can carry unpaired
    # UTF-16 surrogates (e.g. half of a mathematical-bold pair); a strict
    # encode raises and takes down the whole conversation loop. The hash only
    # needs deterministic bytes, not valid UTF-8.
    return hashlib.sha256(value.encode("utf-8", "surrogatepass")).hexdigest()


# ---------------------------------------------------------------------------
# Progressive Evaluation & Multi-Level Authorization Guardrails (Req 1, 3, 6, 14)
# ---------------------------------------------------------------------------

_GREETING_WORDS = frozenset({
    "hola", "buenos dias", "buenos días", "buenas tardes", "buenas noches",
    "hey", "hi", "hello", "que tal", "qué tal", "como estas", "cómo estás",
    "como va", "cómo va", "saludos", "buenas", "que mas", "qué más"
})

_ACK_WORDS = frozenset({
    "gracias", "muchas gracias", "ok", "okay", "vale", "entendido", "perfecto",
    "buenísimo", "buenisimo", "de acuerdo", "excelente", "dale", "listo"
})

_SPEED_OR_PING_PATTERN = re.compile(
    r"\b(?:prueba|test|testear|probar)\s+(?:de\s+)?(?:velocidad|latencia|respuesta|tiempo)|"
    r"(?:medir|mide)\s+(?:el\s+)?tiempo|\bping\b|\bpong\b",
    re.IGNORECASE
)

_FUTURE_INTENTION_PATTERN = re.compile(
    r"\b(?:mañana|luego|después|despues|más tarde|mas tarde|la próxima semana|proxima semana)\s+"
    r"(?:quiero|vamos|hacemos|trabajamos|revisamos|veremos|vemos)\b",
    re.IGNORECASE
)

_FILE_OR_URL_PATTERN = re.compile(
    r"https?://|\b[\w\-\./]+\.(?:py|sh|json|yaml|yml|md|txt|csv|pdf|docx|xlsx|png|jpg|jpeg|mp3|mp4|log|ts|js|html|css)\b|"
    r"(?:^|\s)(?:/[a-zA-Z0-9_\-\.]+)+",
    re.IGNORECASE
)

_ACTION_DIRECTIVES = re.compile(
    r"\b(?:crea|crear|haz|hacer|modifica|modificar|edita|editar|actualiza|actualizar|"
    r"borra|borrar|elimina|eliminar|ejecuta|ejecutar|instala|instalar|configura|configurar|"
    r"busca|buscar|encuentra|analiza|analizar|revisa|revisar|lee|leer|escribe|escribir|"
    r"despliega|deploy|repara|arregla|corrige|reinicia|reiniciar)\b",
    re.IGNORECASE
)

_CONFIRMATION_PATTERNS = re.compile(
    r"\b(?:si|sí|dale|adelante|procede|proceder|confirmo|confirmado|hazlo|ejecuta|ejecútalo|"
    r"yes|ok|okay|proceed|go ahead|aplica|aplicalo|aplícalo|de acuerdo|perfecto procede)\b",
    re.IGNORECASE
)

_MUTATING_OR_DESTRUCTIVE_COMMANDS = re.compile(
    r"""(?:^|\s|&&|\|\||;|`)(?:
        rm\s|rmdir\s|mv\s|cp\s|install\s|sed\s+-i|truncate\s|dd\s|shred\s|
        git\s+(?:commit|push|reset|clean|checkout|rebase|merge)\s|
        docker\s+(?:rm|kill|stop|restart|build|run|compose\s+(?:down|up))\s|
        systemctl\s|service\s|kill\s|pkill\s|shutdown\s|reboot\s|
        pip\s+install|npm\s+(?:install|run\s+build)|apt-get|apt\s
    )""",
    re.VERBOSE | re.IGNORECASE
)

_IMPERATIVE_COMMANDS = re.compile(
    r"\b(?:crea|escribe|modifica|edita|actualiza|borra|elimina|ejecuta|instala|despliega|agrega|cambia|aplica|haz)\b",
    re.IGNORECASE
)


def classify_turn_intent(message_text: str) -> str:
    """Classify the user turn intent as 'conversational' or 'action' with zero latency.

    Enforces:
    - Conversational: Greetings, speed/ping tests, future work planning notes, casual questions, acknowledgements.
    - Action: File attachments, URLs, file paths, imperative code/system modification verbs.
    """
    if not message_text or not isinstance(message_text, str):
        return "action"

    text = message_text.strip()
    if not text:
        return "action"

    # 1. Any file attachment, local path, or URL is an action turn
    if _FILE_OR_URL_PATTERN.search(text):
        return "action"

    # 2. Response speed / latency / ping tests are strictly conversational
    if _SPEED_OR_PING_PATTERN.search(text):
        return "conversational"

    # 3. Clean string for keyword analysis
    clean = re.sub(r"[^\w\s]", " ", text).lower().strip()
    words = clean.split()
    if not words:
        return "action"

    has_action = bool(_ACTION_DIRECTIVES.search(text))

    # 4. If explicit technical action directive is present -> action
    if has_action:
        return "action"

    # 5. Statements of future intention without immediate command -> conversational (Plan Req 3)
    if _FUTURE_INTENTION_PATTERN.search(text):
        return "conversational"

    # 6. Acknowledgements or greetings without actions -> conversational
    has_greeting = any(g in clean for g in _GREETING_WORDS)
    has_ack = any(clean == ack or clean.startswith(ack + " ") or clean.endswith(" " + ack) for ack in _ACK_WORDS)

    if (has_greeting or has_ack) and not has_action:
        return "conversational"

    # 7. Casual questions without action verbs (e.g. "¿cómo estás?", "¿quién eres?")
    is_casual_inquiry = bool(re.match(
        r"^(?:(?:hola|hey|buenas)\b\s*)?(?:¿|\?|quién|quien|cómo|como|qué|que|estas|estás|me escuchas|podes hablar)\b",
        clean,
        re.IGNORECASE
    ))
    if is_casual_inquiry and not has_action:
        return "conversational"

    # Default to action if intent is ambiguous or complex
    return "action"


def is_conversational_turn(message_text: str) -> bool:
    """Check if the user message is a pure greeting or casual chit-chat without an actionable task."""
    return classify_turn_intent(message_text) == "conversational"


def should_decouple_tools_for_turn(
    messages: list[Any],
    tool_turns: int = 0,
    agent: Any = None,
) -> bool:
    """Determine whether tool schemas should be decoupled (tools_for_api = []) for this turn.

    Decoupling saves ~13,600 tokens and ~8-10 seconds of provider latency on conversational turns.
    """
    # 1. Mid-turn tool responses MUST keep tools available
    if tool_turns > 0:
        return False

    if not messages:
        return False

    # 2. Never decouple for cronjobs or autonomous subagents
    if agent is not None:
        if getattr(agent, "is_cron", False) or getattr(agent, "_delegate_depth", 0) > 0:
            return False

    # 3. Check the last message in history
    last_msg = messages[-1]
    last_role = getattr(last_msg, "role", None) if not isinstance(last_msg, dict) else last_msg.get("role")
    if last_role in ("tool", "assistant"):
        # If assistant just called a tool, we cannot decouple
        if isinstance(last_msg, dict) and last_msg.get("tool_calls"):
            return False
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return False

    # 4. Extract last user text
    last_user_text = ""
    for msg in reversed(messages):
        role = getattr(msg, "role", None) if not isinstance(msg, dict) else msg.get("role")
        if role == "user":
            content = getattr(msg, "content", None) if not isinstance(msg, dict) else msg.get("content")
            if isinstance(content, str):
                last_user_text = content
            elif isinstance(content, list):
                # Multipart content (e.g. image, document attachment) -> Keep tools!
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") != "text":
                            return False
                        last_user_text += " " + part.get("text", "")
            break

    if not last_user_text:
        return False

    return classify_turn_intent(last_user_text) == "conversational"


def has_user_confirmation(messages: list[Any]) -> bool:
    """Check if recent user turns contain explicit confirmation or direct imperative command."""
    if not messages:
        return False
    user_turns: list[str] = []
    for msg in reversed(messages):
        role = getattr(msg, "role", None) if not isinstance(msg, dict) else msg.get("role")
        if role == "user":
            content = getattr(msg, "content", None) if not isinstance(msg, dict) else msg.get("content")
            if isinstance(content, str):
                user_turns.append(content)
            elif isinstance(content, list):
                text_parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                user_turns.append(" ".join(text_parts))
            if len(user_turns) >= 3:
                break

    for turn in user_turns:
        clean_turn = turn.strip().lower()
        if _CONFIRMATION_PATTERNS.search(clean_turn):
            return True
        # If the turn is an open question or inquiry, it is NOT an authorization
        is_question = "?" in turn or "¿" in turn or bool(
            re.match(r"^(?:qué|que|cómo|como|cuál|cual|por qué|será|podríamos|podemos)\b", clean_turn)
        )
        if is_question:
            continue
        # Check for direct imperative action command
        if _IMPERATIVE_COMMANDS.search(clean_turn) and len(clean_turn.split()) >= 3:
            return True
    return False


def check_runtime_execution_guardrails(
    agent: Any,
    tool_name: str,
    tool_args: Mapping[str, Any] | None,
    messages: list[Any] | None = None,
) -> tuple[bool, str | None]:
    """Universal runtime interceptor enforcing 5-State Progressive Evaluation and Multi-Level Authorization.

    Enforces:
    - State 1: Suppresses tool executions on pure greetings/chit-chat for immediate conversational Fast Ack (<2s).
    - State 4: Intercepts high-impact mutating actions (file/system edits) until explicit user confirmation is present.
    """
    # 1. Bypass guardrails for cronjobs and autonomous subagent execution
    if getattr(agent, "is_cron", False) or getattr(agent, "_delegate_depth", 0) > 0:
        return False, None

    tool_args = tool_args or {}
    messages = messages or getattr(agent, "messages", []) or []

    # Extract the last user message text
    last_user_text = ""
    for msg in reversed(messages):
        role = getattr(msg, "role", None) if not isinstance(msg, dict) else msg.get("role")
        if role == "user":
            content = getattr(msg, "content", None) if not isinstance(msg, dict) else msg.get("content")
            if isinstance(content, str):
                last_user_text = content
            elif isinstance(content, list):
                parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                last_user_text = " ".join(parts)
            break

    # 2. State 1 Guardrail: Pure Conversation / Casual Greeting
    if is_conversational_turn(last_user_text):
        if tool_name in MUTATING_TOOL_NAMES or tool_name in ("memory", "search_files"):
            reason = (
                "INTERCEPTED (State 1: Pure Conversation): The user sent a casual greeting or conversational message. "
                "Do NOT execute tools, modify files, or scan memory. Respond conversationally, warmly, and immediately."
            )
            return True, reason

    # 3. State 4 Guardrail: Multi-Level Confirmation for High-Impact Actions
    is_high_impact = False
    if tool_name in ("write_file", "patch", "skill_manage", "cronjob_manage"):
        is_high_impact = True
    elif tool_name == "process_manage":
        if str(tool_args.get("action", "")).lower() in ("kill", "terminate", "stop"):
            is_high_impact = True
    elif tool_name in ("terminal", "execute_code"):
        cmd = str(tool_args.get("command") or tool_args.get("code") or "")
        if _MUTATING_OR_DESTRUCTIVE_COMMANDS.search(cmd):
            is_high_impact = True

    if is_high_impact:
        if not has_user_confirmation(messages):
            reason = (
                f"INTERCEPTED (State 4: High-Impact Action Requires Confirmation): "
                f"Tool '{tool_name}' mutates files, code, or systems. "
                f"You MUST first present your execution plan to the user with the proposed changes, "
                f"explain the expected outcome, and ask for explicit authorization ('dale' / 'sí' / 'procede') before executing."
            )
            return True, reason

    return False, None

