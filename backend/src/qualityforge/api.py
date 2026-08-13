from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from qualityforge import __version__
from qualityforge.graph import requirement_from_request, run_pipeline
from qualityforge.llm import configured_model
from qualityforge.models import AgentRun, RunRequest
from qualityforge.settings import get_settings

app = FastAPI(
    title="QualityForge Agent",
    version=__version__,
    description="Plan requirements, map the DOM, generate Playwright tests, and report insights.",
)


class StackStatus(BaseModel):
    app_env: str
    llm_provider: str
    llm_model: str
    vector_backend: str
    database: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/health/stack", response_model=StackStatus)
def stack() -> StackStatus:
    settings = get_settings()
    return StackStatus(
        app_env=settings.app_env,
        llm_provider=settings.llm_provider,
        llm_model=configured_model(settings),
        vector_backend=settings.vector_backend,
        database="postgres",
    )


@app.post("/v1/runs", response_model=AgentRun)
def create_run(request: RunRequest) -> AgentRun:
    requirement = requirement_from_request(
        title=request.title,
        text=request.text,
        requirement_id=request.id,
        jira_key=request.jira_key,
        url=request.url,
    )
    return run_pipeline(requirement, get_settings())
