#!/usr/bin/env node
import { createDefaultPipeline } from "./create-pipeline.js";
import { QualityForgeAgent } from "./orchestrator.js";
import { requirementFromCli } from "./requirement.js";

async function main(): Promise<void> {
  const requirement = requirementFromCli(process.argv.slice(2));
  const agent = new QualityForgeAgent(createDefaultPipeline());
  const run = await agent.run(requirement);

  process.stdout.write(`${JSON.stringify(run, null, 2)}\n`);

  const failed = run.results.some((result) => result.status === "failed");
  process.exitCode = failed ? 1 : 0;
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`${message}\n`);
  process.exitCode = 1;
});
