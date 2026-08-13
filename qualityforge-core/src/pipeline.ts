import type {
  AgentRun,
  DomMap,
  GeneratedTest,
  QualityInsights,
  Requirement,
  TestPlan,
  TestRunResult,
} from "./types.js";

/** Stage contracts. Implementations live in sibling packages; the agent orchestrates. */
export interface PlannerAgent {
  plan(requirement: Requirement): Promise<TestPlan>;
}

export interface DomIntelligence {
  map(requirement: Requirement, plan: TestPlan): Promise<DomMap>;
}

export interface TestGenerator {
  generate(requirement: Requirement, plan: TestPlan, dom: DomMap): Promise<GeneratedTest[]>;
}

export interface PlaywrightExecutor {
  execute(tests: GeneratedTest[], dom: DomMap): Promise<TestRunResult[]>;
}

export interface QualityInsightsAgent {
  analyze(run: Omit<AgentRun, "insights">): Promise<QualityInsights>;
}

export interface AgentPipeline {
  planner: PlannerAgent;
  dom: DomIntelligence;
  generator: TestGenerator;
  executor: PlaywrightExecutor;
  insights: QualityInsightsAgent;
}
