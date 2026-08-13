import pytest

from qualityforge.graph import requirement_from_request, run_pipeline

pytestmark = pytest.mark.unit


def test_pipeline_dry_run() -> None:
    requirement = requirement_from_request(
        title="Shopper can open the cart",
        text="As a shopper I can open the cart from https://example.com",
        requirement_id="QF-1",
        jira_key="QF-1",
    )
    run = run_pipeline(requirement)
    assert run.requirement.jira_key == "QF-1"
    assert run.dom.url == "https://example.com"
    assert run.tests[0].spec
    assert run.results[0].status == "passed"
    assert run.insights.failures == []
    assert "get_by_role" in run.tests[0].spec
