from qualityforge.models import PlannedStep, Requirement, TestPlan
from qualityforge.settings import Settings


def plan_requirement(requirement: Requirement, settings: Settings | None = None) -> TestPlan:
    del settings
    has_url = "http://" in requirement.text or "https://" in requirement.text or bool(requirement.source_url)
    steps = [
        PlannedStep(
            id="analyze",
            capability="requirement-analysis",
            rationale="Normalize the requirement into a testable intent",
        ),
        PlannedStep(
            id="strategy",
            capability="test-strategy",
            rationale="Choose coverage: happy path, negative, and regression guards",
        ),
        PlannedStep(
            id="dom",
            capability="dom-intelligence",
            rationale=(
                "Requirement includes a URL; map landmarks and user-facing locators"
                if has_url
                else "Infer landmarks from the requirement until a crawl target is supplied"
            ),
        ),
        PlannedStep(
            id="generate-and-run",
            capability="playwright",
            rationale="Generate a Playwright spec and execute it through the agent pipeline",
        ),
    ]
    if requirement.jira_key:
        steps.append(
            PlannedStep(
                id="jira",
                capability="jira",
                rationale=f"Keep coverage in sync with {requirement.jira_key}",
            )
        )
    steps.append(
        PlannedStep(
            id="report",
            capability="ci-cd",
            rationale="Emit structured results that CI can gate on",
        )
    )
    return TestPlan(
        requirement_id=requirement.id,
        summary=f'Analyze "{requirement.title}" and produce an executable Playwright path.',
        strategy=[
            "Extract acceptance criteria and risks from the requirement text",
            "Map shopper-facing controls before generating locators",
            "Prefer getByRole / getByLabel over implementation selectors",
            "Dry-run execution first; promote to a live Playwright run in CI",
            "Turn failures into next actions for Quality Insights",
        ],
        steps=steps,
    )
