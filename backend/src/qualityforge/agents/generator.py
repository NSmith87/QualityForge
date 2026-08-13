from qualityforge.models import DomMap, GeneratedTest, Requirement, TestPlan


def _locator_line(dom: DomMap) -> str:
    locator = dom.locators[0] if dom.locators else None
    if locator and locator.role and locator.name:
        return (
            f"    await expect(page.get_by_role({locator.role!r}, name={locator.name!r})"
            ").to_be_visible()"
        )
    if locator and locator.label:
        return f"    await expect(page.get_by_label({locator.label!r})).to_be_visible()"
    return "    await expect(page.get_by_role('main')).to_be_visible()"


def generate_tests(requirement: Requirement, plan: TestPlan, dom: DomMap) -> list[GeneratedTest]:
    del plan
    url = dom.url or "about:blank"
    spec = f'''from playwright.async_api import expect, Page

async def test_{requirement.id.replace("-", "_").lower()}(page: Page) -> None:
    await page.goto({url!r})
{_locator_line(dom)}
'''
    return [
        GeneratedTest(
            id=f"{requirement.id}-e2e-1",
            title=requirement.title,
            spec=spec,
            locators=dom.locators,
        )
    ]
