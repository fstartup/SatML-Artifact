# Microsoft Foundry Project Pilot Runbook

## Purpose

This runbook validates the real-model adapter against a Microsoft Foundry project endpoint before the Scenario A pilot is executed.

The model must never receive direct access to the synthetic environment. The path is:

`Foundry Responses API -> typed tool proposal -> Scenario A Tool Gateway -> deterministic policy -> synthetic environment -> evidence`

## v1.6 continuation fix

The harness uses the Responses API `previous_response_id` continuation pattern for tool calls. After a model emits a function call, the next request sends only the `function_call_output` item and references the prior response ID. This avoids replaying GPT-5 reasoning items into the next request, which can otherwise produce a Foundry `invalid_payload` 400 during multi-turn tool calling. Microsoft documents this continuation pattern for the Responses API.

## Known-good endpoint validation

The following configuration has been validated outside the harness:

- Project endpoint: `https://<resource>.services.ai.azure.com/api/projects/<project>`
- API route: `/openai/v1/responses`
- Deployment: `gpt-5-nano`
- Expected response: `FOUNDRY_TEST_OK`

Do not use `/openai/v1/models` as the health check for this project endpoint.

## Environment

```cmd
set AZURE_OPENAI_API_KEY=<your-key>
set FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
set PYTHONPATH=src
```

Do not paste or commit the API key.

## Single controlled run

From `experiments\\src`:

```cmd
python -m scenario_a.real_model_runner --provider foundry_project --model gpt-5-nano --profile P2 --ticket T103 --seed 0 --max-turns 8 --attack ATK01 --output ..\\results\\real_model_pilot
```

Expected behavior is a JSON result with `PASS` or `OBSERVATION`, plus a run directory containing `events.jsonl`.

A `PASS` means the harness completed the defined safe-task criteria for this synthetic case; it does not establish general model safety.

## If the run is INVALID

Inspect the run's `events.jsonl` for `model_error` only if the run directory was created. Never paste credentials.

If no run directory is created, run the minimal direct Responses test first:

```cmd
python -c "import os; from openai import OpenAI; c=OpenAI(api_key=os.environ['AZURE_OPENAI_API_KEY'],base_url=os.environ['FOUNDRY_PROJECT_ENDPOINT'].rstrip('/')+'/openai/v1/'); print('CLIENT_OK'); r=c.responses.create(model='gpt-5-nano',input='Reply with exactly: FOUNDRY_TEST_OK'); print(r.output_text)"
```

## Pilot sequencing

1. Direct Responses check: PASS
2. Harness single-run tool-call check: PASS/OBSERVATION
3. Tool-gateway/policy boundary check: PASS
4. Only then run the full pilot matrix

Do not connect the harness to production systems, real customer records, real credentials, uncontrolled external agents, or production repositories.
## Budget-conscious paired pilot

Use the paired-only launcher with the default `--repeats 1` for the first validation pass. This produces 4 real-model runs: P1 clean, P1 ATK01, P2 clean, P2 ATK01. Treat the result as trajectory/instrument validation, not a statistical safety claim.

