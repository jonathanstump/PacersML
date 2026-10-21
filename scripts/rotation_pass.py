"""Rotation-only pass (D13): fetch gamerotation for downloaded games that don't have it yet.

The download chunks skip gamerotation while it is cooling down after 5 failures in a row, and cached games go by
in seconds, so most games never got a call. This pass makes the calls instead: one request per try, the same
3.5-4.0 s pace, up to ROTATION_TRIES tries per game in total (the ledger is shared with refresh.py), in rounds,
so a game that failed gets its second try at least one round later.

Outage guard: after OUTAGE_STREAK failures in a row, check the same game's box score on stats.nba.com. If that
fails too, the host is down, not gamerotation: those tries are taken back off the ledger, and the pass pauses
5, 15, 30 minutes, then stops. Rests REST_S after every REST_EVERY requests, like the download chunks.

Resumable: the ledger and every rotation file are written per game. Run it when no other pull is running, then
run refresh.py (normal mode) to process.

    python -u scripts/rotation_pass.py                       # all seasons with downloaded games
    python -u scripts/rotation_pass.py --seasons 2024-25
"""
from __future__ import annotations

import argparse
import json
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

import probe_endpoints  # noqa: E402

OUTAGE_STREAK = 10
PAUSES_S = (300, 900, 1800)
REST_EVERY, REST_S = 400, 1800


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S UTC")


def host_up(gid: str) -> bool:
    """Is stats.nba.com answering for this game's box score? Separates an outage from gamerotation failing."""
    box = next(p for p in probe_endpoints.probes(gid) if p[1] == "boxscoretraditionalv3")
    return probe_endpoints.probe_one(*box)["result"] == "ok"


def todo(season: str, ledger: dict) -> list[str]:
    box_dir = cache.RAW / season / "stats_box"
    gids = sorted(p.name.split(".")[0] for p in box_dir.glob("*.json.gz")) if box_dir.exists() else []
    return [g for g in gids if cache.find_raw(season, ["stats_rotation"], g) is None
            and ledger.get(g, 0) < ROTATION_TRIES]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", nargs="+", default=SEASONS)
    args = ap.parse_args()

    # one request per try, no endpoint cooldown: the outage guard below does that job here
    c = Client(retries=1, cooldown_after=10**9)
    rested_at = 0
    for season in args.seasons:
        path, ledger = rotation_ledger(season)
        rnd = 0
        while games := todo(season, ledger):
            rnd += 1
            n_ok = n_fail = 0
            print(f"\n=== {season} round {rnd}: {len(games)} games without rotation @ {stamp()}", flush=True)
            streak: list[str] = []
            pauses = iter(PAUSES_S)
            i = 0
            while i < len(games):
                gid = games[i]
                if c.n_requests - rested_at >= REST_EVERY:
                    print(f"  resting {REST_S}s after {REST_EVERY} requests @ {stamp()}", flush=True)
                    time.sleep(REST_S)
                    rested_at = c.n_requests
                try:
                    payload = c.stats("gamerotation", {"GameID": gid, "LeagueID": "00"},
                                      timeout=10.0, host_level=False)
                except (EndpointError, EndpointBlocked, FileNotFoundError):
                    ledger[gid] = ledger.get(gid, 0) + 1
                    streak.append(gid)
                    n_fail += 1
                else:
                    cache.write_raw(payload, season, "stats_rotation", gid)
                    streak, n_ok = [], n_ok + 1
                    pauses = iter(PAUSES_S)
                path.write_text(json.dumps(ledger))
                i += 1

                if len(streak) >= OUTAGE_STREAK:
                    if host_up(gid):
                        streak = []  # the host answers: these were gamerotation's own failures, they count
                        continue
                    for g in streak:  # an outage: take these tries back and redo them after the pause
                        ledger[g] -= 1
                    path.write_text(json.dumps(ledger))
                    n_fail -= len(streak)
                    i -= len(streak)
                    streak = []
                    c.blocked_hosts.clear()
                    wait = next(pauses, None)
                    if wait is None:
                        print(f"  stats.nba.com still down after pauses of {PAUSES_S} s; stopping @ {stamp()}")
                        return 3
                    print(f"  stats.nba.com not answering box scores either; pausing {wait}s @ {stamp()}", flush=True)
                    time.sleep(wait)

                if i % 50 == 0:
                    print(f"  {i}/{len(games)} · ok {n_ok} · failed {n_fail} @ {stamp()}", flush=True)
            print(f"  round {rnd} done: ok {n_ok} · failed {n_fail}", flush=True)

        n_rot = len(list((cache.RAW / season / "stats_rotation").glob("*.json.gz")))
        n_box = len(list((cache.RAW / season / "stats_box").glob("*.json.gz")))
        print(f"=== {season}: rotation files for {n_rot}/{n_box} downloaded games", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
