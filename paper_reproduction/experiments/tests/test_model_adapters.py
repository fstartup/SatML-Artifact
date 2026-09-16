import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from model_adapters import OpenAIResponsesAdapter, AnthropicMessagesAdapter, ScenarioAToolGateway, run_model_loop
from scenario_a.environment import ScenarioAEnvironment
from scenario_a.policy import ScenarioAPolicy
from runner import RunRecorder


class Obj:
    def __init__(self, **kw): self.__dict__.update(kw)
    def model_dump(self): return dict(self.__dict__)


class FakeOpenAI:
    def __init__(self): self.calls = 0
    class Responses:
        pass
    @property
    def responses(self):
        outer = self
        class R:
            def create(self, **kwargs):
                outer.calls += 1
                if outer.calls == 1:
                    fc = Obj(type="function_call", call_id="call-1", name="read_ticket", arguments=json.dumps({"ticket_id":"T100"}))
                    return Obj(id="resp-1", status="completed", output=[fc], output_text="")
                return Obj(id="resp-2", status="completed", output=[], output_text="Resolved.")
        return R()


class FakeAnthropic:
    def __init__(self): self.calls = 0
    @property
    def messages(self):
        outer = self
        class M:
            def create(self, **kwargs):
                outer.calls += 1
                if outer.calls == 1:
                    tool = Obj(type="tool_use", id="tool-1", name="read_ticket", input={"ticket_id":"T100"})
                    return Obj(id="msg-1", stop_reason="tool_use", content=[tool], usage=Obj(input_tokens=10, output_tokens=5))
                return Obj(id="msg-2", stop_reason="end_turn", content=[Obj(type="text", text="Resolved.")], usage=Obj(input_tokens=10, output_tokens=5))
        return M()


def test_openai_adapter_parses_function_call():
    result = OpenAIResponsesAdapter("fake", client=FakeOpenAI()).complete(system="s", messages=[{"role":"user","content":"x"}], tools=[])
    assert result.tool_calls[0]["name"] == "read_ticket"
    assert result.tool_calls[0]["arguments"]["ticket_id"] == "T100"
    assert result.raw_output_items[0]["type"] == "function_call"


def test_anthropic_adapter_parses_tool_use():
    result = AnthropicMessagesAdapter("fake", client=FakeAnthropic()).complete(system="s", messages=[{"role":"user","content":"x"}], tools=[])
    assert result.tool_calls[0]["name"] == "read_ticket"
    assert result.tool_calls[0]["arguments"]["ticket_id"] == "T100"


def test_real_model_loop_keeps_tool_execution_behind_gateway(tmp_path):
    env = ScenarioAEnvironment(); env.reset(0)
    recorder = RunRecorder(tmp_path)
    gateway = ScenarioAToolGateway(env, ScenarioAPolicy(), "test-agent", "P2", recorder)
    adapter = OpenAIResponsesAdapter("fake", client=FakeOpenAI())
    result = run_model_loop(adapter, system="s", user_message="Read T100", tools=[], gateway=gateway, recorder=recorder, max_turns=2)
    assert result.text == "Resolved."
    assert env.tickets["T100"].status == "open"
    events = (recorder.path / "events.jsonl").read_text().splitlines()
    assert any('"event_type": "action_proposal"' in e for e in events)
    assert any('"event_type": "execution"' in e for e in events)
