# QualityForge engineering stack

MVP stack matches the agent pipeline: plan, map the DOM, generate Playwright, execute, and store knowledge.

## Backend

Python 3.11+ in `backend/`.

| Layer | Choice |
|---|---|
| API | FastAPI |
| Agent graph | LangGraph (CrewAI optional extra for multi-agent crews) |
| Models | Pydantic / pydantic-settings |
| Database | Postgres |

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
qualityforge run --title "Shopper can open the cart" --text "As a shopper I can open the cart from https://example.com"
qualityforge serve
```

API:

- `GET /health`
- `GET /health/stack`
- `POST /v1/runs`

## AI

| Environment | Provider | Models |
|---|---|---|
| Local | Ollama | Mistral / Llama (`LLM_MODEL=mistral`) |
| Production | OpenAI API | `OPENAI_MODEL` |
| Production | Anthropic API | `ANTHROPIC_MODEL` |
| Production | Azure OpenAI | deployment + endpoint |

Set `LLM_PROVIDER` to `ollama`, `openai`, `anthropic`, or `azure_openai`. Copy `.env.example` to `.env`. The planner still dry-runs without a live LLM.

Local Ollama:

```bash
ollama serve
ollama pull mistral
```

## Browser automation

Playwright (Python). The MVP executor is a dry-run: it emits a spec and structured results without launching a browser. Live execution uses the same `execute_tests` contract.

## Vector store

Start simple: **ChromaDB** (`VECTOR_BACKEND=chroma`, on-disk at `CHROMA_PATH`).

Move later (optional extras in `backend/pyproject.toml`):

- Qdrant
- Pinecone
- Weaviate

## Postgres

```bash
docker compose up -d postgres
```

Default URL: `postgresql+psycopg://qualityforge:qualityforge@127.0.0.1:5432/qualityforge`

## Secrets

Never commit `.env`, tokens, or provider keys. CI uses dry-run defaults only.

## GitLab CI

Target project: [qualityforge-group/QualityForge-project](https://gitlab.com/qualityforge-group/QualityForge-project).

```
GitLab CI
    |
    ├── Unit tests
    ├── Playwright tests
    ├── AI evaluation tests
    └── Deployment
```

| Stage | Jobs | What runs |
|---|---|---|
| `unit` | `unit:python`, `unit:node` | Pytest unit markers; Node build + agent dry-run |
| `playwright` | `playwright:agent`, `playwright:live` | Generated Playwright spec checks; live Chromium is manual / `PLAYWRIGHT_LIVE=1` |
| `ai_eval` | `ai_eval:agent` | Plan coverage, user-facing locators, actionable insights |
| `deploy` | `deploy:staging`, `deploy:production` | Staging package on default branch; production is manual |

Config: `.gitlab-ci.yml` includes `ci/unit.yml`, `ci/playwright.yml`, `ci/ai-eval.yml`, `ci/deploy.yml`.

```bash
git remote add gitlab git@gitlab.com:qualityforge-group/QualityForge-project.git
```
