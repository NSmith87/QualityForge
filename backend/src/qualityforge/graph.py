from __future__ import annotations

from typing import Any, TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from qualityforge.agents.dom import map_dom
from qualityforge.agents.executor import execute_tests
from qualityforge.agents.generator import generate_tests
from qualityforge.agents.insights import analyze_run
from qualityforge.agents.planner import plan_requirement
from qualityforge.models import (
    AgentRun,
    DomMap,
    GeneratedTest,
    QualityInsights,
    Requirement,
    TestPlan,
    TestRunResult,
)
from qualityforge.settings import Settings, get_settings


class AgentState(TypedDict, total=False):
    requirement: dict[str, Any]
    plan: dict[str, Any]
    dom: dict[str, Any]
    tests: list[dict[str, Any]]
    results: list[dict[str, Any]]
    insights: dict[str, Any]


def _planner(state: AgentState) -> dict[str, Any]:
    requirement = Requirement.model_validate(state["requirement"])
    plan = plan_requirement(requirement)
    return {"plan": plan.model_dump()}


def _dom(state: AgentState) -> dict[str, Any]:
    requirement = Requirement.model_validate(state["requirement"])
    plan = TestPlan.model_validate(state["plan"])
    return {"dom": map_dom(requirement, plan).model_dump()}


def _generate(state: AgentState) -> dict[str, Any]:
    requirement = Requirement.model_validate(state["requirement"])
    plan = TestPlan.model_validate(state["plan"])
    dom = DomMap.model_validate(state["dom"])
    tests = generate_tests(requirement, plan, dom)
    return {"tests": [test.model_dump() for test in tests]}


def _execute(state: AgentState) -> dict[str, Any]:
    tests = [GeneratedTest.model_validate(item) for item in state["tests"]]
    dom = DomMap.model_validate(state["dom"])
    results = execute_tests(tests, dom)
    return {"results": [result.model_dump() for result in results]}


def _insights(state: AgentState) -> dict[str, Any]:
    run = AgentRun(
        requirement=Requirement.model_validate(state["requirement"]),
        plan=TestPlan.model_validate(state["plan"]),
        dom=DomMap.model_validate(state["dom"]),
        tests=[GeneratedTest.model_validate(item) for item in state["tests"]],
        results=[TestRunResult.model_validate(item) for item in state["results"]],
        insights=QualityInsights(summary="", failures=[], next_actions=[]),
    )
    return {"insights": analyze_run(run).model_dump()}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", _planner)
    graph.add_node("dom", _dom)
    graph.add_node("generator", _generate)
    graph.add_node("executor", _execute)
    graph.add_node("insights", _insights)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "dom")
    graph.add_edge("dom", "generator")
    graph.add_edge("generator", "executor")
    graph.add_edge("executor", "insights")
    graph.add_edge("insights", END)
    return graph.compile()


PIPELINE = build_graph()


def requirement_from_request(
    title: str,
    text: str | None = None,
    requirement_id: str | None = None,
    jira_key: str | None = None,
    url: str | None = None,
) -> Requirement:
    body = text or title
    return Requirement(
        id=requirement_id or jira_key or str(uuid4()),
        title=title,
        text=body,
        jira_key=jira_key,
        source_url=url,
    )


def run_pipeline(requirement: Requirement, settings: Settings | None = None) -> AgentRun:
    del settings
    result = PIPELINE.invoke({"requirement": requirement.model_dump()})
    return AgentRun.model_validate(
        {
            "requirement": result["requirement"],
            "plan": result["plan"],
            "dom": result["dom"],
            "tests": result["tests"],
            "results": result["results"],
            "insights": result["insights"],
        }
    )


def run_from_cli(title: str, text: str | None = None, **kwargs: str | None) -> AgentRun:
    requirement = requirement_from_request(title=title, text=text, **kwargs)
    return run_pipeline(requirement, get_settings())
