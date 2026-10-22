"""Rotation-only pass (D13, revised D15): fetch gamerotation for downloaded games that don't have it yet.

The download chunks never call gamerotation; this pass makes every call: one request per try, up to
ROTATION_TRIES tries per game in total (the ledger is shared with refresh.py), in rounds, so a game that failed
gets its second try at least one round later.

Pace and throttle guard (D15): gamerotation throttles us on its own while other endpoints keep answering
(2026-10-22: 13 of 14 calls timed out or 500'd, including games that had downloaded fine, while box scores
answered in < 1 s). So:
  - one gamerotation call every INTERVAL_S seconds (default 30);
  - when a call fails, ask gamerotation for a CANARY game we already have. Canary answers -> the failure is the
    game's own and counts as one of its tries. Canary fails too -> we are being throttled: the try is not
    counted, and the pass backs off BACKOFF_S (30 min, 1 h, 2 h, 4 h), then stops.

Resumable: the ledger and every rotation file are written per game. Run it when no other pull is running, then
run refresh.py (normal mode) to process.

    python -u scripts/rotation_pass.py                       # all seasons with downloaded games
    python -u scripts/rotation_pass.py --seasons 2024-25 --interval 45
    python -u scripts/rotation_pass.py --reset-throttled     # once: clear tries recorded before D15 (see below)
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pacersml.data import cache  # noqa: E402
from pacersml.data.http import Client, EndpointBlocked, EndpointError  # noqa: E402
from refresh import ROTATION_TRIES, SEASONS, rotation_ledger  # noqa: E402

INTERVAL_S = 30
BACKOFF_S = (1800, 3600, 7200, 14400)
UNAVAILABLE = (EndpointError, EndpointBlocked, FileNotFoundError)


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S UTC")


def todo(season: str, ledger: dict) -> list[str]:
    box_dir = cache.RAW / season / "stats_box"
    gids = sorted(p.name.split(".")[0] for p in box_dir.glob("*.json.gz")) if box_dir.exists() else []
    return [g for g in gids if cache.find_raw(season, ["stats_rotation"], g) is None
            and ledger.get(g, 0) < ROTATION_TRIES]


def canary(season: str) -> str | None:
    rot = sorted((cache.RAW / season / "stats_rotation").glob("*.json.gz"))
    return rot[0].name.split(".")[0] if rot else None


def reset_throttled(seasons: list[str]) -> None:
    """Tries recorded before D15 were made while gamerotation was throttling us, so they say nothing about the
    games. Back the ledger up and clear it for games still without a rotation file."""
    for season in seasons:
        path, ledger = rotation_ledger(season)
        if not ledger:
            continue
        shutil.copy(path, path.with_name("rotation_attempts_pre_d15.json"))
        kept = {g: n for g, n in ledger.items() if cache.find_raw(season, ["stats_rotation"], g) is not None}
        path.write_text(json.dumps(kept))
        print(f"{season}: cleared {len(ledger) - len(kept)} recorded tries (backup rotation_attempts_pre_d15.json)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", nargs="+", default=SEASONS)
    ap.add_argument("--interval", type=float, default=INTERVAL_S, help="seconds between gamerotation calls")
    ap.add_argument("--reset-throttled", action="store_true", help="clear pre-D15 tries, then exit")
    args = ap.parse_args()
    if args.reset_throttled:
        reset_throttled(args.seasons)
        return 0

    # one request per try, no endpoint cooldown: the canary below decides whether a failure counts
    c = Client(min_interval=args.interval, retries=1, cooldown_after=10**9)

    def call(gid: str):
        return c.stats("gamerotation", {"GameID": gid, "LeagueID": "00"}, timeout=10.0, host_level=False)

    for season in args.seasons:
        path, ledger = rotation_ledger(season)
        ref = canary(season) or canary("2024-25")
        rnd = 0
        while games := todo(season, ledger):
            rnd += 1
            n_ok = n_fail = n_throttled = 0
            print(f"\n=== {season} round {rnd}: {len(games)} games without rotation · canary {ref} @ {stamp()}",
                  flush=True)
            backoffs = iter(BACKOFF_S)
            i = 0
            while i < len(games):
                gid = games[i]
                try:
                    payload = call(gid)
                except UNAVAILABLE:
                    c.blocked_hosts.clear()
                    try:
                        call(ref)
                    except UNAVAILABLE:  # the canary fails too: throttled, the try doesn't count
                        c.blocked_hosts.clear()
                        n_throttled += 1
                        wait = next(backoffs, None)
                        if wait is None:
                            print(f"  gamerotation still throttling after backoffs of {BACKOFF_S} s; "
                                  f"stopping @ {stamp()} (resume later with the same command)")
                            return 3
                        print(f"  {gid}: failed and canary {ref} failed too: throttled, not counted; "
                              f"backing off {wait}s @ {stamp()}", flush=True)
                        time.sleep(wait)
                        continue  # retry the same game
                    ledger[gid] = ledger.get(gid, 0) + 1  # canary answered: this game's own failure
                    n_fail += 1
                else:
                    cache.write_raw(payload, season, "stats_rotation", gid)
                    n_ok += 1
                    backoffs = iter(BACKOFF_S)
                path.write_text(json.dumps(ledger))
                i += 1
                if i % 25 == 0:
                    print(f"  {i}/{len(games)} · ok {n_ok} · failed {n_fail} · throttled {n_throttled} @ {stamp()}",
                          flush=True)
            print(f"  round {rnd} done: ok {n_ok} · failed {n_fail} · throttled {n_throttled}", flush=True)

        n_rot = len(list((cache.RAW / season / "stats_rotation").glob("*.json.gz")))
        n_box = len(list((cache.RAW / season / "stats_box").glob("*.json.gz")))
        print(f"=== {season}: rotation files for {n_rot}/{n_box} downloaded games", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
