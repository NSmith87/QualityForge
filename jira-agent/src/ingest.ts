import type { Requirement } from "@qualityforge/core";

export interface JiraIssueInput {
  key: string;
  summary: string;
  description?: string;
  url?: string;
}

export function requirementFromJira(issue: JiraIssueInput): Requirement {
  return {
    id: issue.key,
    title: issue.summary,
    text: issue.description?.trim() || issue.summary,
    jiraKey: issue.key,
    sourceUrl: issue.url,
  };
}
