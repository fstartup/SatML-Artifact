import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from model_adapters import FoundryProjectResponsesAdapter, run_model_loop, ScenarioAToolGateway
from scenario_a.environment import ScenarioAEnvironment
from scenario_a.policy import ScenarioAPolicy
from runner import RunRecorder


class Obj:
    def __init__(self, **kw): self.__dict__.update(kw)
    def model_dump(self): return dict(self.__dict__)


class FakeFoundry:
    def __init__(self): self.calls = 0; self.kwargs = []
    @property
    def responses(self):
        outer = self
        class R:
            def create(self, **kwargs):
                outer.calls += 1; outer.kwargs.append(kwargs)
                if outer.calls == 1:
                    reasoning = Obj(type="reasoning", summary=[], encrypted_content="opaque")
                    fc = Obj(type="function_call", call_id="call-1", name="read_ticket", arguments=json.dumps({"ticket_id":"T103"}))
                    return Obj(id="resp-1", status="completed", output=[reasoning, fc], output_text="")
                return Obj(id="resp-2", status="completed", output=[], output_text="Resolved safely.")
        return R()


def test_foundry_adapter_is_first_class_responses_provider():
    fake = FakeFoundry()
    adapter = FoundryProjectResponsesAdapter("gpt-5-nano", client=fake)
    assert adapter.provider == "foundry_project"
    assert adapter.endpoint_type == "project"
    result = adapter.complete(system="s", messages=[{"role":"user","content":"x"}], tools=[])
    assert result.tool_calls[0]["name"] == "read_ticket"


def test_foundry_provider_uses_openai_responses_tool_loop(tmp_path):
    env = ScenarioAEnvironment(); env.reset(0)
    recorder = RunRecorder(tmp_path)
    gateway = ScenarioAToolGateway(env, ScenarioAPolicy(), "foundry-gpt-5-nano", "P2", recorder)
    fake = FakeFoundry()
    adapter = FoundryProjectResponsesAdapter("gpt-5-nano", client=fake)
    result = run_model_loop(adapter, system="s", user_message="Read T103", tools=[], gateway=gateway, recorder=recorder, max_turns=2)
    assert result.text == "Resolved safely."
    assert fake.calls == 2
    assert fake.kwargs[1]["previous_response_id"] == "resp-1"
    assert fake.kwargs[1]["input"] == [{"type": "function_call_output", "call_id": "call-1", "output": "{\"ticket\": \"T103\"}"}] or any(item.get("type") == "function_call_output" for item in fake.kwargs[1]["input"])
    assert not any(item.get("type") == "reasoning" for item in fake.kwargs[1]["input"])
