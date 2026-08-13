import { HeuristicDomIntelligence } from "@qualityforge/dom-intelligence";
import { DryRunPlaywrightExecutor, PlaywrightTestGenerator } from "@qualityforge/playwright-agent";
import type { AgentPipeline } from "@qualityforge/core";
import { HeuristicQualityInsights } from "./insights.js";
import { HeuristicPlanner } from "./planner.js";

export function createDefaultPipeline(): AgentPipeline {
  return {
    planner: new HeuristicPlanner(),
    dom: new HeuristicDomIntelligence(),
    generator: new PlaywrightTestGenerator(),
    executor: new DryRunPlaywrightExecutor(),
    insights: new HeuristicQualityInsights(),
  };
}
