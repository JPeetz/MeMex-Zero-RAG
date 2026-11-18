#!/usr/bin/env python3
"""Fail when a secret-shaped string appears that the baseline has not already reviewed.

Why not `detect-secrets scan --baseline`: its filtering semantics vary by version and it
silently emitted non-JSON in this pipeline. Comparing the two JSON documents directly is
boring, deterministic, and does not hide an error behind `|| true`.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / ".secrets.baseline"


def scan() -> dict:
    # the baseline itself records hashes of the findings it knows about, so it must not
    # be scanned — otherwise it flags itself forever
    out = subprocess.run([sys.executable, "-m", "detect_secrets", "scan",
                          "--force-use-all-plugins",
                          "--exclude-files", r"\.secrets\.baseline"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout.strip():
        print("detect-secrets produced no output — treating as failure", file=sys.stderr)
        print(out.stderr[-800:], file=sys.stderr)
        sys.exit(2)
    return json.loads(out.stdout).get("results", {})


def fingerprint(results: dict) -> set:
    return {(f, i["line_number"], i["hashed_secret"])
            for f, items in results.items() for i in items}


def main() -> int:
    current = scan()
    known = json.loads(BASELINE.read_text()).get("results", {}) if BASELINE.exists() else {}
    new = fingerprint(current) - fingerprint(known)
    if new:
        print(f"{len(new)} NEW potential secret(s):")
        for f, line, _ in sorted(new):
            print(f"  {f}:{line}")
        print("\nIf reviewed and safe, regenerate: python -m detect_secrets scan "
              "--force-use-all-plugins > .secrets.baseline")
        return 1
    print(f"secret scan: {len(fingerprint(current))} known, 0 new")
    return 0


if __name__ == "__main__":
    sys.exit(main())
