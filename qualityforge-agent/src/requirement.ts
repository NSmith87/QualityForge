import type { Requirement } from "@qualityforge/core";
import { requirementFromJira } from "@qualityforge/jira-agent";
import { randomUUID } from "node:crypto";

export function requirementFromCli(args: string[]): Requirement {
  const flags = parseFlags(args);
  const title = flags.title ?? "Untitled requirement";
  const text = flags.text ?? title;
  const jiraKey = flags.jira;
  const id = flags.id ?? jiraKey ?? randomUUID();

  if (jiraKey) {
    return requirementFromJira({
      key: jiraKey,
      summary: title,
      description: text,
      url: flags.url,
    });
  }

  return {
    id,
    title,
    text,
    sourceUrl: flags.url,
  };
}

function parseFlags(args: string[]): Record<string, string> {
  const flags: Record<string, string> = {};

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = args[i + 1];
    if (!next || next.startsWith("--")) {
      flags[key] = "true";
      continue;
    }
    flags[key] = next;
    i += 1;
  }

  return flags;
}
