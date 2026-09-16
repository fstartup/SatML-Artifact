# Azure OpenAI / Microsoft Foundry Real-Model Pilot Runbook

## Recommended setup
Use the Azure OpenAI v1-compatible endpoint first:

- `AZURE_OPENAI_API_KEY` = Azure API key
- `AZURE_OPENAI_ENDPOINT` = `https://<resource>.openai.azure.com`
- `--endpoint-type azure`
- `--model <deployment-name>`

Microsoft documents the OpenAI Python client with `base_url=https://<resource>.openai.azure.com/openai/v1/` and `client.responses.create(...)`.

## Foundry project endpoint
For a Foundry project:

- `AZURE_OPENAI_API_KEY` = project/API key if enabled for the endpoint
- `FOUNDRY_PROJECT_ENDPOINT` = `https://<resource>.services.ai.azure.com/api/projects/<project>`
- `--provider foundry_project`

The harness appends `/openai/v1/`.

## Windows CMD
Do not paste the secret into the repository or into ChatGPT. If the existing variable is `OPEN_AI_KEY`, temporarily map it:

```cmd
set AZURE_OPENAI_API_KEY=%OPEN_AI_KEY%
set AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
```

Verify without printing the secret:

```cmd
python -c "import os; print('AZURE_OPENAI_API_KEY=', 'SET' if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT_SET'); print('AZURE_OPENAI_ENDPOINT=', 'SET' if os.getenv('AZURE_OPENAI_ENDPOINT') else 'NOT_SET')"
```

Run one controlled test first:

```cmd
set PYTHONPATH=src
python -m scenario_a.real_model_runner --provider azure_openai --endpoint-type azure --model YOUR_DEPLOYMENT_NAME --profile P2 --ticket T103 --seed 0 --max-turns 8 --attack ATK01 --output experiments\results\real_model_pilot
```

Only after the single run is valid should the 42-run pilot be started.

## Security boundary
The real model receives only synthetic Scenario A context and typed tool definitions. Tool calls are routed through the synthetic Scenario A gateway and policy layer. No production system, customer record, credential, or uncontrolled external tool may be connected.
