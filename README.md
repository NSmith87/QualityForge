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

## Intended flow

```
Jira story  →  jira-agent (ingest ACs)
            →  rag-engine (similar tests / gaps)
            →  dom-intelligence (page map)
            →  playwright-agent (draft + run)
            →  jira-agent (Tests, executions, status)
            →  qualityforge-ui (review)
```

`qualityforge-agent` owns that sequence. `qualityforge-core` is the shared language between steps.

## Status

Scaffolding. Packages are not published yet.

## License

UNLICENSED until published.
