export type RunStatus = "passed" | "failed" | "skipped";

export interface Requirement {
  id: string;
  title: string;
  text: string;
  jiraKey?: string;
  sourceUrl?: string;
}

export interface PlannedStep {
  id: string;
  capability: string;
  rationale: string;
}

export interface TestPlan {
  requirementId: string;
  summary: string;
  strategy: string[];
  steps: PlannedStep[];
}

export interface LocatorHypothesis {
  role?: string;
  name?: string;
  label?: string;
  rationale: string;
}

export interface DomMap {
  url?: string;
  landmarks: string[];
  locators: LocatorHypothesis[];
}

export interface GeneratedTest {
  id: string;
  title: string;
  spec: string;
  locators: LocatorHypothesis[];
}

export interface TestRunResult {
  testId: string;
  status: RunStatus;
  durationMs: number;
  error?: string;
  diagnostics: string[];
}

export interface QualityInsights {
  summary: string;
  failures: string[];
  nextActions: string[];
}

export interface AgentRun {
  requirement: Requirement;
  plan: TestPlan;
  dom: DomMap;
  tests: GeneratedTest[];
  results: TestRunResult[];
  insights: QualityInsights;
}
