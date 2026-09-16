# Foundry Anthropic / Claude Haiku 4.5 — Scenario A Matched-Model Runbook

## Purpose

Run exactly two additional real-model calls to compare Claude Haiku 4.5 with the existing GPT-5-nano P2 paired results. The only intended experimental variable is the model deployment.

Microsoft Foundry Claude deployments use the Anthropic Messages API at the dedicated `/anthropic` endpoint, not the OpenAI-compatible `/openai/v1` endpoint. The deployment name is supplied as the `model` field.

## Deployment

- Deployment: `claude-haiku-4-5`
- Foundry resource: same resource used by the existing GPT deployment
- Base endpoint: `https://<resource>.services.ai.azure.com/anthropic`

## Credentials

Use an environment variable; never place a key in source control or command history. Preferred names:

```cmd
set AZURE_API_KEY=<your-key>
```

The adapter also accepts `ANTHROPIC_FOUNDRY_API_KEY`. For convenience in this research harness it can fall back to the existing Azure/OpenAI-named variables if those are the credentials accepted by the resource.

## Two-call experiment

From `experiments/src`:

### H1 — clean

```cmd
python -m scenario_a.real_model_runner --provider foundry_anthropic --model claude-haiku-4-5 --profile P2 --ticket T103 --seed 0 --max-turns 8 --output ..\results\haiku_p2
```

### H2 — ATK01

```cmd
python -m scenario_a.real_model_runner --provider foundry_anthropic --model claude-haiku-4-5 --profile P2 --ticket T103 --seed 0 --max-turns 8 --attack ATK01 --output ..\results\haiku_p2
```

Do not run P1, additional repeats, or additional attacks unless the paper's experimental design is explicitly expanded.

## Expected evidence

Compare the two Haiku runs with the existing GPT-5-nano P2 clean/ATK01 pair on:

- update-ticket status selected
- prohibited action proposed
- prohibited action executed
- blocked prohibited action
- refund count
- account unchanged
- tool errors
- turn limit
- objective-deviation observation

Do not infer causality or rank model safety from one matched pair. The purpose is to establish whether model behavior differs while the deterministic action-control boundary remains the same.

## Security boundary

The model receives only synthetic Scenario A data. It has no direct access to production systems, credentials, real customer data, or external tools. All tool calls pass through `ScenarioAToolGateway` and the Scenario A policy layer.

## Source

Microsoft Foundry documentation confirms that Claude uses the Anthropic Messages API and a dedicated endpoint of the form `https://<resource>.services.ai.azure.com/anthropic`, with the deployment name used as the model identifier.
