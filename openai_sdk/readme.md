
## Install Dependencies
To enable support for other LLMs, install the required dependencies:
```bash
uv pip install "openai-agents[litellm]"
```

### Run Manager Agent
To run the manager agent, use the following command:
```bash
uv run src/02_manager_agent.py
```

### Run Guardrails Agent
To run the guardrails agent, use the following command:
```bash
uv run src/03_guardrails.py
```
**Notes**
- Ensure that all required environment variables are set in the `.env` file.
- Refer to the documentation for additional configuration options.
