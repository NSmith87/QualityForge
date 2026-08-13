import type { PlannerAgent, Requirement, TestPlan } from "@qualityforge/core";

const CAPABILITIES = {
  analysis: "requirement-analysis",
  strategy: "test-strategy",
  dom: "dom-intelligence",
  playwright: "playwright",
  jira: "jira",
  cicd: "ci-cd",
} as const;

export class HeuristicPlanner implements PlannerAgent {
  async plan(requirement: Requirement): Promise<TestPlan> {
    const needsJira = Boolean(requirement.jiraKey);
    const hasUrl = /https?:\/\//i.test(requirement.text);

    return {
      requirementId: requirement.id,
      summary: `Analyze "${requirement.title}" and produce an executable Playwright path.`,
      strategy: [
        "Extract acceptance criteria and risks from the requirement text",
        "Map shopper-facing controls before generating locators",
        "Prefer getByRole / getByLabel over implementation selectors",
        "Dry-run execution first; promote to a live Playwright run in CI",
        "Turn failures into next actions for Quality Insights",
      ],
      steps: [
        {
          id: "analyze",
          capability: CAPABILITIES.analysis,
          rationale: "Normalize the requirement into a testable intent",
        },
        {
          id: "strategy",
          capability: CAPABILITIES.strategy,
          rationale: "Choose coverage: happy path, negative, and regression guards",
        },
        {
          id: "dom",
          capability: CAPABILITIES.dom,
          rationale: hasUrl
            ? "Requirement includes a URL; map landmarks and user-facing locators"
            : "Infer landmarks from the requirement until a crawl target is supplied",
        },
        {
          id: "generate-and-run",
          capability: CAPABILITIES.playwright,
          rationale: "Generate a Playwright spec and execute it through the agent pipeline",
        },
        ...(needsJira
          ? [
              {
                id: "jira",
                capability: CAPABILITIES.jira,
                rationale: `Keep coverage in sync with ${requirement.jiraKey}`,
              },
            ]
          : []),
        {
          id: "report",
          capability: CAPABILITIES.cicd,
          rationale: "Emit structured results that CI can gate on",
        },
      ],
    };
  }
}
