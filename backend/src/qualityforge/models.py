from typing import Literal

from pydantic import BaseModel, Field

RunStatus = Literal["passed", "failed", "skipped"]


class Requirement(BaseModel):
    id: str
    title: str
    text: str
    jira_key: str | None = None
    source_url: str | None = None


class PlannedStep(BaseModel):
    id: str
    capability: str
    rationale: str


class TestPlan(BaseModel):
    requirement_id: str
    summary: str
    strategy: list[str]
    steps: list[PlannedStep]


class LocatorHypothesis(BaseModel):
    role: str | None = None
    name: str | None = None
    label: str | None = None
    rationale: str


class DomMap(BaseModel):
    url: str | None = None
    landmarks: list[str] = Field(default_factory=list)
    locators: list[LocatorHypothesis] = Field(default_factory=list)


class GeneratedTest(BaseModel):
    id: str
    title: str
    spec: str
    locators: list[LocatorHypothesis] = Field(default_factory=list)


class TestRunResult(BaseModel):
    test_id: str
    status: RunStatus
    duration_ms: int
    error: str | None = None
    diagnostics: list[str] = Field(default_factory=list)


class QualityInsights(BaseModel):
    summary: str
    failures: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class AgentRun(BaseModel):
    requirement: Requirement
    plan: TestPlan
    dom: DomMap
    tests: list[GeneratedTest]
    results: list[TestRunResult]
    insights: QualityInsights


class RunRequest(BaseModel):
    title: str
    text: str | None = None
    id: str | None = None
    jira_key: str | None = None
    url: str | None = None
