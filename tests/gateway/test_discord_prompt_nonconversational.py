"""Discord prompt cards must be non-conversational.

Clarify, exec-approval and slash-confirm cards (plus operational notices) are
UI, not conversation.  Their message IDs must be registered with the
non-conversational tracker so they neither partition the Discord history
backfill nor leak into the reply-window context.  Prompt cards are sent
through ``channel.send`` directly (bypassing ``send()``'s metadata handling),
so each sender must register the ID itself.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

_repo = str(Path(__file__).resolve().parents[2])
if _repo not in sys.path:
    sys.path.insert(0, _repo)

from plugins.platforms.discord.adapter import (  # noqa: E402
    DiscordAdapter,
    _looks_like_nonconversational_history_message,
)
from gateway.config import PlatformConfig  # noqa: E402


def _make_adapter():
    config = PlatformConfig(enabled=True, token="test-token", extra={})
    adapter = DiscordAdapter(config)
    adapter._client = MagicMock()
    adapter._allowed_user_ids = set()
    adapter._allowed_role_ids = set()
    return adapter


def _channel_returning(message_id: int) -> MagicMock:
    channel = MagicMock()
    sent = MagicMock()
    sent.id = message_id
    channel.send = AsyncMock(return_value=sent)
    return channel


# ---------------------------------------------------------------------------
# Legacy recognizer (messages emitted before IDs were tracked)
# ---------------------------------------------------------------------------

def test_prompt_cards_are_recognized_as_nonconversational():
    assert _looks_like_nonconversational_history_message(
        "❓ **Hermes needs your input**\n\n¿Cómo procedemos con el Lote 0?"
    )
    assert _looks_like_nonconversational_history_message(
        "⚠️ **Command Approval Required**\n\nDo you want Hermes to run this command?"
    )
    assert _looks_like_nonconversational_history_message(
        '⚠️ Subagent failed — "Clasificar el destino…" (after 1472s)'
    )


def test_normal_conversation_is_not_recognized():
    assert not _looks_like_nonconversational_history_message(
        "¡Listo, muchacho! 🐢 Terminé el informe y quedó todo verificado."
    )


# ---------------------------------------------------------------------------
# Senders register the message ID
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_send_clarify_registers_message_as_nonconversational():
    adapter = _make_adapter()
    adapter._client.get_channel = MagicMock(return_value=_channel_returning(987654))

    result = await adapter.send_clarify(
        chat_id="9001",
        question="Pick a color",
        choices=["red", "green"],
        clarify_id="cid1",
        session_key="sk1",
    )

    assert result.success is True
    assert "987654" in adapter._nonconversational_messages


@pytest.mark.asyncio
async def test_open_ended_clarify_registers_message_as_nonconversational():
    adapter = _make_adapter()
    adapter._client.get_channel = MagicMock(return_value=_channel_returning(222333))

    result = await adapter.send_clarify(
        chat_id="9001",
        question="What is your name?",
        choices=None,
        clarify_id="cid2",
        session_key="sk2",
    )

    assert result.success is True
    assert "222333" in adapter._nonconversational_messages


@pytest.mark.asyncio
async def test_send_exec_approval_registers_message_as_nonconversational():
    adapter = _make_adapter()
    adapter._client.get_channel = MagicMock(return_value=_channel_returning(555444))

    result = await adapter.send_exec_approval(
        chat_id="9001",
        command="rm -rf /tmp/example",
        session_key="sk3",
        description="dangerous command",
    )

    assert result.success is True
    assert "555444" in adapter._nonconversational_messages


@pytest.mark.asyncio
async def test_send_slash_confirm_registers_message_as_nonconversational():
    adapter = _make_adapter()
    adapter._client.get_channel = MagicMock(return_value=_channel_returning(111222))

    result = await adapter.send_slash_confirm(
        chat_id="9001",
        title="Confirm",
        message="Proceed?",
        session_key="sk4",
        confirm_id="cf1",
    )

    assert result.success is True
    assert "111222" in adapter._nonconversational_messages
