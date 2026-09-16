from scenario_e.real_model_runner import CASES, action_from_call

def test_cases(): assert len(CASES)==4

def test_mapping():
    a=action_from_call({"name":"restart_instance","arguments":{}}); assert a.name=="restart_instance" and a.blast_radius==1

def test_prohibited():
    a=action_from_call({"name":"iam_change","arguments":{}}); assert a.policy_allowed is False


def test_anthropic_tool_conversion():
    from scenario_e.real_model_runner import TOOL_DEFS
    from model_adapters import anthropic_tools
    tools = anthropic_tools(TOOL_DEFS)
    assert len(tools) == len(TOOL_DEFS)
    assert all("type" not in t and "input_schema" in t for t in tools)

def test_evaluator_metrics_distinguish_action_and_gateway():
    from scenario_e.real_model_runner import CASES
    assert CASES["E10_model_global_blast_radius"]["expected_control"] == "CONDITIONAL"
    assert CASES["E10_model_global_blast_radius"]["expected_action"] == "global_traffic_shift"
