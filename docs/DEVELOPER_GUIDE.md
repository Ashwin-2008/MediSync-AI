# Developer Guide

## Local Setup
1. `pip install -r backend/requirements.txt`
2. Start Redis: `docker run -d -p 6379:6379 redis`
3. Export API Keys: `export OPENAI_API_KEY="sk-..."`
4. Start FastAPI: `uvicorn backend.main:app --reload`
5. Start Celery: `celery -A backend.workers.tasks worker --loglevel=info`

## Adding a New Agent
To add a new agent, you do not need to write boilerplate logic.
1. Run `python scripts/generate_agents.py --name "SocialWorkAgent"`.
2. This generates the scaffolding in `agents/roles/social_work/`.
3. Provide few-shot examples in `prompts/examples.md`.
4. Register the agent in `orchestrator/planner.py`.

## Adding a New Tool
1. Define the Pydantic input/output schemas in `agents/shared/tools/schemas.py`.
2. Implement the static method in `agents/shared/tools/implementations.py`.
3. The `ToolPlanner` will automatically discover the tool if registered in `ToolRegistry`.

## Testing
Run the evaluation benchmark:
```bash
python -m evaluation.benchmark_runner
```
This simulates load and computes cost metrics.
