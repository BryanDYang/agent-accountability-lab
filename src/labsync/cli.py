"""Initial CLI entry point. Meeting processing is not implemented yet."""

import argparse
import json
from importlib.metadata import version


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="labsync", description="Meeting follow-through assistant"
    )
    parser.add_argument("--version", action="version", version=version("ai-capstone"))
    commands = parser.add_subparsers(dest="command", required=True)
    status = commands.add_parser(
        "status", help="Show implementation and service status"
    )
    status.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    args = parser.parse_args(argv)
    state = {
        "version": version("ai-capstone"),
        "implementation": "scaffold",
        "service": "not_implemented",
        "meeting_processing": "not_implemented",
    }
    if args.json:
        print(json.dumps(state))
    else:
        print(f"LabSync {state['version']} - repository scaffold")
        print("Background service and meeting processing are not implemented yet.")
    return 0
