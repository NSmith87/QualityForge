import type { DomIntelligence, DomMap, Requirement, TestPlan } from "@qualityforge/core";

function inferUrl(requirement: Requirement): string | undefined {
  const match = requirement.text.match(/https?:\/\/[^\s)]+/i);
  return match?.[0];
}

export class HeuristicDomIntelligence implements DomIntelligence {
  async map(requirement: Requirement, plan: TestPlan): Promise<DomMap> {
    const locators = plan.steps
      .filter((step) => step.capability === "playwright")
      .map((step) => ({
        role: "button",
        name: requirement.title,
        rationale: `User-facing control inferred from planned step ${step.id}`,
      }));

    return {
      url: inferUrl(requirement),
      landmarks: ["main", "navigation"],
      locators:
        locators.length > 0
          ? locators
          : [
              {
                role: "heading",
                name: requirement.title,
                rationale: "Fallback landmark until a live crawl is wired",
              },
            ],
    };
  }
}
