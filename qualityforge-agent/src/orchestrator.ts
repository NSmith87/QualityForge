import type { AgentPipeline, AgentRun, Requirement } from "@qualityforge/core";

export class QualityForgeAgent {
  constructor(private readonly pipeline: AgentPipeline) {}

  async run(requirement: Requirement): Promise<AgentRun> {
    const plan = await this.pipeline.planner.plan(requirement);
    const dom = await this.pipeline.dom.map(requirement, plan);
    const tests = await this.pipeline.generator.generate(requirement, plan, dom);
    const results = await this.pipeline.executor.execute(tests, dom);
    const insights = await this.pipeline.insights.analyze({
      requirement,
      plan,
      dom,
      tests,
      results,
    });

    return { requirement, plan, dom, tests, results, insights };
  }
}
