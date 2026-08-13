import type { AgentRun, QualityInsights, QualityInsightsAgent } from "@qualityforge/core";

export class HeuristicQualityInsights implements QualityInsightsAgent {
  async analyze(run: Omit<AgentRun, "insights">): Promise<QualityInsights> {
    const failures = run.results
      .filter((result) => result.status === "failed")
      .map((result) => result.error ?? `${result.testId} failed`);

    const nextActions = failures.length
      ? [
          "Inspect Playwright diagnostics and traces for the failing spec",
          "Re-map DOM locators if the control was not found",
          "Re-run after the locator or fixture is corrected",
        ]
      : [
          "Promote the dry-run spec to a live Playwright job in CI",
          run.requirement.jiraKey
            ? `Link the generated test and execution back to ${run.requirement.jiraKey}`
            : "Attach a Jira key on the next run to enable coverage write-back",
        ];

    const passed = run.results.filter((result) => result.status === "passed").length;
    const total = run.results.length;

    return {
      summary: `${passed}/${total} tests passed for ${run.requirement.id}. Strategy: ${run.plan.strategy[0] ?? "n/a"}`,
      failures,
      nextActions,
    };
  }
}
