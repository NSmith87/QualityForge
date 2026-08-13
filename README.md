# QualityForge

AI-assisted quality engineering platform: turn requirements into tests, understand the product in the browser, and keep Jira / execution in sync.

This repository is a monorepo. Each top-level directory is a product surface with a clear owner.

```
QualityForge/
│
├── qualityforge-agent      Main AI orchestration platform
├── qualityforge-core       Shared libraries and models
├── dom-intelligence        Browser crawling + DOM understanding engine
├── playwright-agent        AI test generation + execution
├── jira-agent              Requirements → tests → Jira automation
├── rag-engine              Embeddings, retrieval, knowledge base
├── qualityforge-ui         Web dashboard
├── docs                    Public and private documentation
└── website                 QualityForge.dev marketing site
```

## Packages

### `qualityforge-agent`

Main AI orchestration platform.

Coordinates the other agents: when to crawl, retrieve, generate, execute, and write back to Jira. Owns run plans, tool routing, and session state. Other packages do not call each other directly; they go through this layer.

### `qualityforge-core`

Shared libraries and models.

Types, contracts, and utilities used across agents (story / AC / test / execution models, config, logging, auth helpers). No product UI and no Jira- or Playwright-specific I/O here.

### `dom-intelligence`

Browser crawling and DOM understanding engine.

Builds a shopper-facing map of the app: landmarks, roles, labels, and stable locators. Prefer user-facing signals (`getByRole`, `getByLabel`) over implementation hooks. Feeds `playwright-agent` and the RAG index.

### `playwright-agent`

AI test generation and execution.

Turns coverage gaps and DOM maps into Playwright specs, runs them, and returns structured results (pass / fail / skip, traces, diagnostics). Does not own Jira issue lifecycle.

### `jira-agent`

Requirements → tests → Jira automation.

Ingests stories and acceptance criteria, publishes Xray Tests, links coverage, records Test Executions, and updates ticket status. Consumes orchestration decisions; does not generate Playwright files itself.

### `rag-engine`

Embeddings, retrieval, and knowledge base.

Indexes stories, tests, DOM snapshots, and docs. Serves similar-test / similar-AC retrieval for generation, duplication checks, and coverage analysis.

### `qualityforge-ui`

Web dashboard.

Run status, coverage, review queues, and agent activity. Talks to `qualityforge-agent` APIs, not to Jira or browsers directly.

### `docs`

Public and private documentation.

Architecture, how-tos, and operator runbooks. Keep secrets out of public docs.

### `website`

[QualityForge.dev](https://qualityforge.dev) marketing site.

Positioning, product pages, and public docs entry points. Separate from `qualityforge-ui` (the product app).

## Agent pipeline

```
Requirements
     |
     v
Planner Agent
     |
     v
DOM Intelligence
     |
     v
Test Generator
     |
     v
Playwright Executor
     |
     v
Quality Insights
```

`qualityforge-agent` owns that sequence. `qualityforge-core` is the shared language between steps. Sibling packages implement a stage; they do not call each other directly.

### Capabilities

- Requirement analysis
- Test strategy generation
- DOM intelligence
- Playwright automation
- Failure analysis
- Jira integration
- CI/CD integration

### Run locally

TypeScript CLI (existing scaffold):

```bash
npm install
npm run build
npm run agent -- --title "Shopper can open the cart" --text "As a shopper I can open the cart from https://example.com"
```

Python MVP agent (FastAPI + LangGraph):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
qualityforge run --title "Shopper can open the cart" --text "As a shopper I can open the cart from https://example.com"
qualityforge serve
```

The first pipeline is a dry-run: it plans, maps locators, emits a Playwright spec, and reports insights without launching a browser.

## GitLab CI

[qualityforge-group/QualityForge-project](https://gitlab.com/qualityforge-group/QualityForge-project)

```
GitLab CI
    |
    ├── Unit tests
    ├── Playwright tests
    ├── AI evaluation tests
    └── Deployment
```

## Engineering stack

See [docs/ENGINEERING.md](docs/ENGINEERING.md).

| Layer | MVP | Later |
|---|---|---|
| Backend | Python, FastAPI, LangGraph, Pydantic, Postgres | CrewAI crews |
| AI (local) | Ollama, Mistral / Llama | — |
| AI (prod) | OpenAI, Anthropic, Azure OpenAI | — |
| Browser | Playwright | live traces |
| Vector | ChromaDB | Qdrant, Pinecone, Weaviate |

## Status

Runnable TypeScript scaffold plus Python FastAPI/LangGraph agent. Live crawls, live Playwright, and Jira write-back are next. Packages are not published yet.

## License

UNLICENSED until published.
