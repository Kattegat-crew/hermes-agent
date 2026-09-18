"""Resolved prompt cards collapse into one-line records.

Clarify cards must stop sitting in the chat as stale, still-actionable
surveys: after the answer (or timeout) the card is edited to a compact record
showing the question and the answer/action.  These tests cover the record text,
the future→card-id plumbing, and the Discord edit that clears the embed and
the interactive components.
"""

import concurrent.futures
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

_repo = str(Path(__file__).resolve().parents[2])
if _repo not in sys.path:
    sys.path.insert(0, _repo)

from gateway.config import PlatformConfig  # noqa: E402
from gateway.run import (  # noqa: E402
    _clarify_resolution_record,
    _compact_prompt_card,
    _prompt_card_message_id,
    _truncate_prompt_field,
)
from plugins.platforms.discord.adapter import DiscordAdapter  # noqa: E402


@pytest.fixture(autouse=True)
def _default_language(monkeypatch):
    monkeypatch.delenv("HERMES_LANGUAGE", raising=False)


class _FakePromptAdapter:
    """Adapter double whose *class* exposes the prompt-edit capability."""

    def __init__(self):
        self.calls = []

    async def edit_prompt_resolution(
        self, chat_id, message_id, content, *, metadata=None
    ):
        self.calls.append((chat_id, message_id, content))


def test_truncate_collapses_whitespace_and_caps():
    assert _truncate_prompt_field("  hola   mundo \n") == "hola mundo"
    out = _truncate_prompt_field("x" * 200, limit=20)
    assert len(out) == 20
    assert out.endswith("…")


def test_clarify_record_answered():
    line = _clarify_resolution_record("¿Modo?", "Modo TODO", timeout_minutes=60)
    assert "¿Modo?" in line
    assert "Modo TODO" in line
    assert "✅" in line


def test_clarify_record_timeout_hides_sentinel():
    line = _clarify_resolution_record(
        "¿Firma?", "[user did not respond within 60m]", timeout_minutes=60
    )
    assert "⌛" in line
    assert "60 min" in line
    assert "did not respond" not in line


def test_clarify_record_spanish(monkeypatch):
    monkeypatch.setenv("HERMES_LANGUAGE", "es")
    answered = _clarify_resolution_record("¿Modo?", "Modo TODO", timeout_minutes=60)
    timeout = _clarify_resolution_record("¿Modo?", "[timeout]", timeout_minutes=60)
    assert "Respondiste" in answered
    assert "Quedó sin respuesta" in timeout


def test_prompt_card_message_id_reads_completed_future():
    fut = concurrent.futures.Future()
    fut.set_result(SimpleNamespace(message_id="123"))
    assert _prompt_card_message_id(fut) == "123"
    assert _prompt_card_message_id(None) is None
    assert _prompt_card_message_id(concurrent.futures.Future()) is None


def test_prompt_resolved_catalog_renders_without_leftovers(monkeypatch):
    from agent.i18n import t

    cases = {
        "prompt_resolved.clarify_answered": {"question": "q", "answer": "a"},
        "prompt_resolved.clarify_timeout": {"question": "q", "minutes": 60},
        "prompt_resolved.approval_approved": {"scope": "s", "command": "c"},
        "prompt_resolved.approval_denied": {"command": "c"},
        "prompt_resolved.approval_expired": {"command": "c"},
        "prompt_resolved.confirm_accepted": {"title": "t"},
        "prompt_resolved.confirm_cancelled": {"title": "t"},
    }
    for lang in ("en", "es"):
        monkeypatch.setenv("HERMES_LANGUAGE", lang)
        for key, kwargs in cases.items():
            text = t(key, **kwargs)
            assert "{" not in text, (lang, key, text)
            for value in kwargs.values():
                assert str(value) in text, (lang, key, text)


@pytest.mark.asyncio
async def test_compact_prompt_card_edits_through_adapter():
    adapter = _FakePromptAdapter()
    await _compact_prompt_card(adapter, "9001", "55", "✅ línea")
    assert adapter.calls == [("9001", "55", "✅ línea")]


@pytest.mark.asyncio
async def test_compact_prompt_card_skips_unsupported_adapter():
    await _compact_prompt_card(SimpleNamespace(), "9001", "55", "✅ línea")


@pytest.mark.asyncio
async def test_compact_prompt_card_ignores_missing_id():
    adapter = _FakePromptAdapter()
    await _compact_prompt_card(adapter, "9001", None, "✅ línea")
    assert adapter.calls == []


@pytest.mark.asyncio
async def test_discord_edit_prompt_resolution_clears_embed_and_view():
    adapter = DiscordAdapter(PlatformConfig(enabled=True, token="t", extra={}))
    adapter._client = MagicMock()
    channel = MagicMock()
    partial = MagicMock()
    partial.edit = AsyncMock()
    channel.get_partial_message = MagicMock(return_value=partial)
    adapter._client.get_channel = MagicMock(return_value=channel)

    result = await adapter.edit_prompt_resolution("9001", "55", "✅ listo")

    assert result.success is True
    partial.edit.assert_awaited_once()
    kwargs = partial.edit.call_args.kwargs
    assert kwargs.get("embed") is None
    assert kwargs.get("view") is None
    assert "✅ listo" in kwargs.get("content", "")


# ---------------------------------------------------------------------------
# Exec-approval card resolution (button + timeout)
# ---------------------------------------------------------------------------

def _make_interaction(*, user_id="42"):
    user = SimpleNamespace(id=user_id, display_name="Tester", roles=[])
    response = SimpleNamespace(
        edit_message=AsyncMock(),
        send_message=AsyncMock(),
        defer=AsyncMock(),
    )
    return SimpleNamespace(user=user, response=response, message=None)


def _approval_view(**kwargs):
    from plugins.platforms.discord import adapter as adapter_mod

    defaults = dict(
        session_key="sk-approval",
        allowed_user_ids={"42"},
        command="rm -rf /tmp/example",
    )
    defaults.update(kwargs)
    return adapter_mod.ExecApprovalView(**defaults)


@pytest.mark.asyncio
async def test_exec_approval_button_leaves_compact_record(monkeypatch):
    import tools.approval as approval_mod

    monkeypatch.setattr(approval_mod, "resolve_gateway_approval", lambda *a, **k: 1)
    view = _approval_view()
    interaction = _make_interaction()

    await view._resolve(interaction, "once")

    interaction.response.edit_message.assert_awaited_once()
    kwargs = interaction.response.edit_message.call_args.kwargs
    assert kwargs.get("embed") is None
    assert kwargs.get("view") is None
    content = kwargs.get("content", "")
    assert "rm -rf /tmp/example" in content
    assert "✅" in content


@pytest.mark.asyncio
async def test_exec_approval_deny_leaves_compact_record(monkeypatch):
    import tools.approval as approval_mod

    monkeypatch.setattr(approval_mod, "resolve_gateway_approval", lambda *a, **k: 1)
    view = _approval_view()
    interaction = _make_interaction()

    await view._resolve(interaction, "deny")

    content = interaction.response.edit_message.call_args.kwargs.get("content", "")
    assert "🚫" in content
    assert "rm -rf /tmp/example" in content


@pytest.mark.asyncio
async def test_exec_approval_timeout_leaves_compact_record():
    view = _approval_view()
    view._message = MagicMock()
    view._message.edit = AsyncMock()

    await view.on_timeout()

    view._message.edit.assert_awaited_once()
    kwargs = view._message.edit.call_args.kwargs
    assert kwargs.get("embed") is None
    assert kwargs.get("view") is None
    content = kwargs.get("content", "")
    assert "⌛" in content
    assert "rm -rf /tmp/example" in content


@pytest.mark.asyncio
async def test_slash_confirm_button_leaves_compact_record(monkeypatch):
    from plugins.platforms.discord import adapter as adapter_mod

    async def _fake_resolve(session_key, confirm_id, choice):
        return ""

    monkeypatch.setattr("tools.slash_confirm.resolve", _fake_resolve, raising=False)

    view = adapter_mod.SlashConfirmView(
        session_key="sk-confirm",
        confirm_id="cf1",
        allowed_user_ids={"42"},
        title="Recargar MCP",
    )
    interaction = _make_interaction()

    await view._resolve(interaction, "cancel")

    kwargs = interaction.response.edit_message.call_args.kwargs
    assert kwargs.get("embed") is None
    assert kwargs.get("view") is None
    content = kwargs.get("content", "")
    assert "Recargar MCP" in content
    assert "🚫" in content


@pytest.mark.asyncio
async def test_slash_confirm_timeout_leaves_compact_record():
    from plugins.platforms.discord import adapter as adapter_mod

    view = adapter_mod.SlashConfirmView(
        session_key="sk-confirm",
        confirm_id="cf2",
        allowed_user_ids={"42"},
        title="Recargar MCP",
    )
    view._message = MagicMock()
    view._message.edit = AsyncMock()

    await view.on_timeout()

    content = view._message.edit.call_args.kwargs.get("content", "")
    assert "⌛" in content
    assert "Recargar MCP" in content
