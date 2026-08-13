import type {
  DomMap,
  GeneratedTest,
  Requirement,
  TestGenerator,
  TestPlan,
} from "@qualityforge/core";

function locatorLine(dom: DomMap): string {
  const locator = dom.locators[0];
  if (locator?.role && locator.name) {
    return `    await expect(page.getByRole('${locator.role}', { name: ${JSON.stringify(locator.name)} })).toBeVisible();`;
  }
  if (locator?.label) {
    return `    await expect(page.getByLabel(${JSON.stringify(locator.label)})).toBeVisible();`;
  }
  return `    await expect(page.getByRole('main')).toBeVisible();`;
}

export class PlaywrightTestGenerator implements TestGenerator {
  async generate(
    requirement: Requirement,
    plan: TestPlan,
    dom: DomMap,
  ): Promise<GeneratedTest[]> {
    const url = dom.url ?? "about:blank";
    const spec = `import { test, expect } from '@playwright/test';

test(${JSON.stringify(requirement.title)}, async ({ page }) => {
    await page.goto(${JSON.stringify(url)});
${locatorLine(dom)}
});
`;

    return [
      {
        id: `${requirement.id}-e2e-1`,
        title: requirement.title,
        spec,
        locators: dom.locators,
      },
    ];
  }
}
