import type { DomMap, GeneratedTest, PlaywrightExecutor, TestRunResult } from "@qualityforge/core";

export class DryRunPlaywrightExecutor implements PlaywrightExecutor {
  async execute(tests: GeneratedTest[], dom: DomMap): Promise<TestRunResult[]> {
    const started = Date.now();

    return tests.map((test) => ({
      testId: test.id,
      status: "passed" as const,
      durationMs: Math.max(1, Date.now() - started),
      diagnostics: [
        "dry-run: Playwright was not launched",
        `target: ${dom.url ?? "unspecified"}`,
        `spec-bytes: ${test.spec.length}`,
      ],
    }));
  }
}
