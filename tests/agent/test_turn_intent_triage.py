"""Unit tests for turn intent triage and dynamic tool decoupling (TDD).

Enforces:
- Conversational turns (greetings, response speed tests, chit-chat, future work notes)
  are classified as 'conversational' so tool schemas (~13k tokens) can be decoupled.
- Action turns (imperative commands, file inspections, code edits, attachments)
  are classified as 'action' so all tools remain available.
- Mid-turn tool executions never decouple tools.
"""

from agent.tool_guardrails import classify_turn_intent, should_decouple_tools_for_turn


def test_greetings_classified_as_conversational():
    assert classify_turn_intent("Hola") == "conversational"
    assert classify_turn_intent("Buenos días Roshi") == "conversational"
    assert classify_turn_intent("Hola Roshi, ¿cómo estás?") == "conversational"
    assert classify_turn_intent("Qué tal todo por ahí?") == "conversational"
    assert classify_turn_intent("buenas noches!") == "conversational"


def test_speed_and_ping_tests_classified_as_conversational():
    assert classify_turn_intent("Prueba de velocidad de respuesta") == "conversational"
    assert (
        classify_turn_intent(
            "Hola Roshi. Este mensaje es para probar tu velocidad de respuesta"
        )
        == "conversational"
    )
    assert classify_turn_intent("test de velocidad") == "conversational"
    assert classify_turn_intent("ping") == "conversational"


def test_future_work_and_acknowledgements_classified_as_conversational():
    # User Plan Requirement 3: statements of future work are conversational, not immediate execution
    assert (
        classify_turn_intent(
            "Hola Roshi, mañana quiero que trabajemos en los videos de Golden."
        )
        == "conversational"
    )
    assert classify_turn_intent("Perfecto, muchas gracias") == "conversational"
    assert classify_turn_intent("Dale, entendido") == "conversational"
    assert classify_turn_intent("Ok, después vemos eso") == "conversational"


def test_action_tasks_classified_as_action():
    assert classify_turn_intent("Lee el archivo config.yaml") == "action"
    assert classify_turn_intent("Revisa el log /var/log/syslog") == "action"
    assert (
        classify_turn_intent("Crea un script en python para ordenar la lista")
        == "action"
    )
    assert (
        classify_turn_intent("Busca en el proyecto dónde se define AIAgent")
        == "action"
    )
    assert classify_turn_intent("Ejecuta los tests de pytest") == "action"
    assert (
        classify_turn_intent("Hola Roshi, podés editar el archivo index.html?")
        == "action"
    )
    assert (
        classify_turn_intent("Modifica la función de login para validar el email")
        == "action"
    )


def test_attachment_or_file_paths_classified_as_action():
    assert classify_turn_intent("Hola, te paso el archivo reporte.pdf") == "action"
    assert classify_turn_intent("Mirá este archivo: datos.xlsx") == "action"
    assert classify_turn_intent("https://github.com/Kattegat-crew/hermes") == "action"


def test_should_decouple_tools_for_turn_evaluates_conversation_state():
    # Fresh greeting turn with tool_turns=0 or tool_turns=1 (1-indexed api_call_count in conversation loop)
    messages = [{"role": "user", "content": "Hola Roshi!"}]
    assert should_decouple_tools_for_turn(messages, tool_turns=0) is True
    assert should_decouple_tools_for_turn(messages, tool_turns=1) is True

    # Speed test with tool_turns=1
    messages = [
        {"role": "user", "content": "Prueba de velocidad de respuesta"}
    ]
    assert should_decouple_tools_for_turn(messages, tool_turns=0) is True
    assert should_decouple_tools_for_turn(messages, tool_turns=1) is True

    # Action task
    messages = [{"role": "user", "content": "Leé el archivo README.md"}]
    assert should_decouple_tools_for_turn(messages, tool_turns=0) is False
    assert should_decouple_tools_for_turn(messages, tool_turns=1) is False

    # Mid-turn tool execution (even if previous user message was conversational)
    messages = [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": None, "tool_calls": [{"id": "1", "function": {"name": "read_file"}}]},
        {"role": "tool", "tool_call_id": "1", "content": "file contents"},
    ]
    assert should_decouple_tools_for_turn(messages, tool_turns=1) is False

    # Subsequent API call within the same turn (tool_turns > 1)
    messages = [{"role": "user", "content": "Hola Roshi!"}]
    assert should_decouple_tools_for_turn(messages, tool_turns=2) is False
