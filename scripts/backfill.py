"""Chunked backfill (D12): download in chunks with long breaks, then one normal refresh that processes everything.

NBA stopped answering twice after ~260-300 new games pulled in one sitting, so the backfill downloads at most
CHUNK games that need the network per run (`refresh.py --max-fetch`), rests BREAK_S, and repeats until nothing is
left to fetch. Each chunk is its own process, so memory is released between chunks. Then the normal refresh runs
from the cache (validation, quarantine, per-100, freezing).

    python -u scripts/backfill.py                      # all three seasons
    python -u scripts/backfill.py --chunk 150 --break-s 2700

Stops (and passes refresh's exit code through) on anything other than 0 or 5.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFRESH = [sys.executable, "-u", str(ROOT / "scripts" / "refresh.py")]
EXIT_CHUNK = 5


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", nargs="+")
    ap.add_argument("--chunk", type=int, default=200, help="games needing the network per chunk")
    ap.add_argument("--break-s", type=int, default=1800, help="rest between chunks, seconds")
    args = ap.parse_args()
    seasons = ["--seasons", *args.seasons] if args.seasons else []

    n = 0
    while True:
        n += 1
        print(f"\n##### chunk {n} @ {stamp()}", flush=True)
        code = subprocess.call(REFRESH + seasons + ["--max-fetch", str(args.chunk)])
        if code == 0:
            break
        if code != EXIT_CHUNK:
            print(f"##### chunk {n} exited {code}; stopping the backfill", flush=True)
            return code
        print(f"##### chunk {n} done; resting {args.break_s}s", flush=True)
        time.sleep(args.break_s)

    print(f"\n##### everything downloaded; processing refresh @ {stamp()}", flush=True)
    return subprocess.call(REFRESH + seasons)


if __name__ == "__main__":
    sys.exit(main())
