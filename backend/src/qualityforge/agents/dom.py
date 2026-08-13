import re

from qualityforge.models import DomMap, LocatorHypothesis, Requirement, TestPlan


def map_dom(requirement: Requirement, plan: TestPlan) -> DomMap:
    url = requirement.source_url
    if not url:
        match = re.search(r"https?://[^\s)]+", requirement.text, re.IGNORECASE)
        url = match.group(0) if match else None

    locators = [
        LocatorHypothesis(
            role="button",
            name=requirement.title,
            rationale=f"User-facing control inferred from planned step {step.id}",
        )
        for step in plan.steps
        if step.capability == "playwright"
    ]
    if not locators:
        locators = [
            LocatorHypothesis(
                role="heading",
                name=requirement.title,
                rationale="Fallback landmark until a live crawl is wired",
            )
        ]
    return DomMap(url=url, landmarks=["main", "navigation"], locators=locators)
