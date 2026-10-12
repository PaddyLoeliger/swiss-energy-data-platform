import argparse
import json
import os
import sys
from pathlib import Path

from energy_platform.pipeline import ingest, verify


def main() -> int:
    parser = argparse.ArgumentParser(description="Swiss electricity production pipeline")
    parser.add_argument("command", choices=["ingest", "verify"])
    args = parser.parse_args()
    try:
        result = ingest(Path(os.getenv("RAW_DIR", "data/raw"))) if args.command == "ingest" else verify()
    except Exception as exc:
        # Avoid leaking connection strings or credentials in third-party errors.
        print(json.dumps({"event": "pipeline_failed", "error_type": type(exc).__name__}), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0
