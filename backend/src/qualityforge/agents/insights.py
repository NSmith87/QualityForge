from qualityforge.models import AgentRun, QualityInsights


def analyze_run(run: AgentRun) -> QualityInsights:
    failures = [
        result.error or f"{result.test_id} failed"
        for result in run.results
        if result.status == "failed"
    ]
    next_actions = (
        [
            "Inspect Playwright diagnostics and traces for the failing spec",
            "Re-map DOM locators if the control was not found",
            "Re-run after the locator or fixture is corrected",
        ]
        if failures
        else [
            "Promote the dry-run spec to a live Playwright job in CI",
            (
                f"Link the generated test and execution back to {run.requirement.jira_key}"
                if run.requirement.jira_key
                else "Attach a Jira key on the next run to enable coverage write-back"
            ),
        ]
    )
    passed = sum(1 for result in run.results if result.status == "passed")
    return QualityInsights(
        summary=(
            f"{passed}/{len(run.results)} tests passed for {run.requirement.id}. "
            f"Strategy: {run.plan.strategy[0] if run.plan.strategy else 'n/a'}"
        ),
        failures=failures,
        next_actions=next_actions,
    )
