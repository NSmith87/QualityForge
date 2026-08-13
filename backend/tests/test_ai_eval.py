import pytest

from qualityforge.graph import requirement_from_request, run_pipeline

pytestmark = pytest.mark.ai_eval

REQUIRED_CAPABILITIES = {
    "requirement-analysis",
    "test-strategy",
    "dom-intelligence",
    "playwright",
}


def _sample_run():
    requirement = requirement_from_request(
        title="Shopper can open the cart",
        text="As a shopper I can open the cart from https://example.com",
        requirement_id="QF-1",
        jira_key="QF-1",
    )
    return run_pipeline(requirement)


def test_plan_covers_pipeline_capabilities() -> None:
    run = _sample_run()
    capabilities = {step.capability for step in run.plan.steps}
    missing = REQUIRED_CAPABILITIES - capabilities
    assert not missing, f"plan missing capabilities: {sorted(missing)}"


def test_spec_prefers_user_facing_locators() -> None:
    spec = _sample_run().tests[0].spec
    assert "get_by_role" in spec or "get_by_label" in spec
    assert "query_selector" not in spec
    assert "get_by_test_id" not in spec


def test_insights_are_actionable() -> None:
    run = _sample_run()
    assert run.insights.summary
    assert run.insights.next_actions
    assert run.insights.failures == []
    assert run.results[0].status == "passed"
