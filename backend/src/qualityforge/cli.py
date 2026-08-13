from __future__ import annotations

import argparse
import json
import sys

import uvicorn

from qualityforge.graph import requirement_from_request, run_pipeline
from qualityforge.settings import get_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qualityforge")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="Start the FastAPI agent")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)

    run = sub.add_parser("run", help="Execute one agent pipeline")
    run.add_argument("--title", required=True)
    run.add_argument("--text")
    run.add_argument("--id")
    run.add_argument("--jira")
    run.add_argument("--url")

    args = parser.parse_args(argv)

    if args.command == "serve":
        uvicorn.run("qualityforge.api:app", host=args.host, port=args.port, reload=False)
        return 0

    requirement = requirement_from_request(
        title=args.title,
        text=args.text,
        requirement_id=args.id,
        jira_key=args.jira,
        url=args.url,
    )
    result = run_pipeline(requirement, get_settings())
    sys.stdout.write(f"{json.dumps(result.model_dump(), indent=2)}\n")
    failed = any(item.status == "failed" for item in result.results)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
