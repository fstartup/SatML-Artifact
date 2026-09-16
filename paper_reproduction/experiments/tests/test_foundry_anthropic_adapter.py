import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from model_adapters import FoundryAnthropicMessagesAdapter, run_model_loop, ScenarioAToolGateway
from scenario_a.environment import ScenarioAEnvironment
from scenario_a.policy import ScenarioAPolicy
from runner import RunRecorder

class Block:
    def __init__(self, **kw): self.__dict__.update(kw)

class FakeMessages:
    def __init__(self): self.calls=[]
    def create(self, **kwargs):
        self.calls.append(kwargs)
        if len(self.calls)==1:
            return Block(id="msg-1", stop_reason="tool_use", usage=Block(input_tokens=10, output_tokens=5),
                         content=[Block(type="tool_use", id="tool-1", name="read_ticket", input={"ticket_id":"T103"})])
        return Block(id="msg-2", stop_reason="end_turn", usage=Block(input_tokens=20, output_tokens=8),
                     content=[Block(type="text", text="Resolved safely.")])

class FakeClient:
    def __init__(self): self.messages=FakeMessages()

def test_foundry_anthropic_provider():
    fake=FakeClient()
    adapter=FoundryAnthropicMessagesAdapter("claude-haiku-4-5", client=fake)
    assert adapter.provider == "foundry_anthropic"
    assert adapter.model_id == "claude-haiku-4-5"
    assert adapter.complete(system="s", messages=[{"role":"user","content":"x"}], tools=[]).tool_calls[0]["name"] == "read_ticket"

def test_foundry_anthropic_tool_loop(tmp_path):
    env=ScenarioAEnvironment(); env.reset(0)
    recorder=RunRecorder(tmp_path)
    gateway=ScenarioAToolGateway(env, ScenarioAPolicy(), "foundry-anthropic-haiku", "P2", recorder)
    fake=FakeClient()
    adapter=FoundryAnthropicMessagesAdapter("claude-haiku-4-5", client=fake)
    result=run_model_loop(adapter, system="s", user_message="Read T103", tools=[], gateway=gateway, recorder=recorder, max_turns=2)
    assert result.text == "Resolved safely."
    assert len(fake.messages.calls)==2
    assert fake.messages.calls[1]["messages"][-1]["role"] == "user"
    assert fake.messages.calls[1]["messages"][-1]["content"][0]["type"] == "tool_result"
