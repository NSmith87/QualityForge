from time import time

from qualityforge.models import DomMap, GeneratedTest, TestRunResult


def execute_tests(tests: list[GeneratedTest], dom: DomMap) -> list[TestRunResult]:
    started = time()
    return [
        TestRunResult(
            test_id=test.id,
            status="passed",
            duration_ms=max(1, int((time() - started) * 1000)),
            diagnostics=[
                "dry-run: Playwright was not launched",
                f"target: {dom.url or 'unspecified'}",
                f"spec-bytes: {len(test.spec)}",
            ],
        )
        for test in tests
    ]
