"""Probe each data source once and record whether it answers from this machine's network.

One request per endpoint, no retries, 15 s timeout. A timeout is recorded as `blocked` because
stats.nba.com tends to hang rather than refuse when it blocks an IP range.

Writes reports/access_probe/{label}_{utc timestamp}.json and, under GitHub Actions, a table in the job summary.
Only depends on `requests` so the workflow installs nothing else.

    python scripts/probe_endpoints.py --label laptop
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

TIMEOUT = 15
SEASON = "2025-26"
GAME_ID = "0022500005"  # IND, 2025-26
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
# Same header set as src/pacersml/data/http.py. The sec-* headers decide whether NBA answers (2026-10-20);
# probes before that date ran without them (header_set "v1").
HEADER_SET = "v2-sec-fetch"
BROWSER = {
    "User-Agent": UA, "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate", "Referer": "https://www.nba.com/", "Origin": "https://www.nba.com",
    "sec-ch-ua": '"Google Chrome";v="141", "Chromium";v="141", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site",
}
STATS_HEADERS = {**BROWSER, "Host": "stats.nba.com", "x-nba-stats-origin": "stats", "x-nba-stats-token": "true"}
CDN_HEADERS = BROWSER
DASH = {
    "Season": SEASON, "SeasonType": "Regular Season", "LeagueID": "00", "PerMode": "Per100Possessions",
    "MeasureType": "Base", "PaceAdjust": "N", "PlusMinus": "N", "Rank": "N", "LastNGames": "0", "Month": "0",
    "OpponentTeamID": "0", "Period": "0", "DateFrom": "", "DateTo": "", "GameSegment": "", "Location": "",
    "Outcome": "", "SeasonSegment": "", "VsConference": "", "VsDivision": "", "TeamID": "0",
}

PROBES = [
    # (source, endpoint label, url, params, headers)
    ("stats.nba.com", "leaguegamelog", "https://stats.nba.com/stats/leaguegamelog",
     {"Counter": 1000, "DateFrom": "", "DateTo": "", "Direction": "ASC", "LeagueID": "00",
      "PlayerOrTeam": "T", "Season": SEASON, "SeasonType": "Regular Season", "Sorter": "DATE"}, STATS_HEADERS),
    ("stats.nba.com", "leaguedashplayerstats_per100", "https://stats.nba.com/stats/leaguedashplayerstats",
     DASH, STATS_HEADERS),
    ("stats.nba.com", "gamerotation", "https://stats.nba.com/stats/gamerotation",
     {"GameID": GAME_ID, "LeagueID": "00"}, STATS_HEADERS),
    ("stats.nba.com", "playbyplayv3", "https://stats.nba.com/stats/playbyplayv3",
     {"GameID": GAME_ID, "StartPeriod": 0, "EndPeriod": 0}, STATS_HEADERS),
    ("stats.nba.com", "boxscoretraditionalv3", "https://stats.nba.com/stats/boxscoretraditionalv3",
     {"GameID": GAME_ID, "StartPeriod": 0, "EndPeriod": 0, "StartRange": 0, "EndRange": 0, "RangeType": 0},
     STATS_HEADERS),
    ("cdn.nba.com", "liveData_playbyplay",
     f"https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{GAME_ID}.json", None, CDN_HEADERS),
    ("cdn.nba.com", "liveData_boxscore",
     f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{GAME_ID}.json", None, CDN_HEADERS),
    ("cdn.nba.com", "scheduleLeagueV2",
     "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json", None, CDN_HEADERS),
    ("pbpstats.com", "get-games", "https://api.pbpstats.com/get-games/nba",
     {"Season": SEASON, "SeasonType": "Regular Season"}, {"User-Agent": UA}),
]


def probe_one(source, endpoint, url, params, headers) -> dict:
    t0 = time.monotonic()
    row = {"source": source, "endpoint": endpoint, "status": None, "latency_s": None, "bytes": 0,
           "json": False, "result": "", "error": ""}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        row.update(status=r.status_code, bytes=len(r.content))
        try:
            r.json()
            row["json"] = True
        except ValueError:
            pass
        row["result"] = "ok" if r.status_code == 200 and row["json"] else "refused"
    except requests.Timeout:
        row.update(result="blocked", error="timeout")
    except requests.RequestException as e:
        row.update(result="blocked", error=f"{type(e).__name__}: {e}"[:200])
    row["latency_s"] = round(time.monotonic() - t0, 2)
    return row


def network_owner() -> str:
    # Organisation name only (no IP is stored); helps compare campus / home / cloud runs.
    try:
        return requests.get("https://ipinfo.io/json", timeout=10).json().get("org", "unknown")
    except requests.RequestException:
        return "unknown"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="github-actions" if os.getenv("GITHUB_ACTIONS") else "local")
    ap.add_argument("--out", default="reports/access_probe")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    rows = [probe_one(*p) for p in PROBES]
    out = {"label": args.label, "utc": now.isoformat(timespec="seconds"), "network": network_owner(),
           "platform": platform.platform(), "header_set": HEADER_SET, "timeout_s": TIMEOUT, "game_id": GAME_ID, "results": rows}

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{args.label}_{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    path.write_text(json.dumps(out, indent=2))

    lines = [f"### Access probe: {args.label} @ {out['utc']} ({out['network']})", "",
             "| source | endpoint | result | status | latency_s | bytes | error |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['source']} | {r['endpoint']} | {r['result']} | {r['status']} | {r['latency_s']} | "
              f"{r['bytes']} | {r['error']} |" for r in rows]
    table = "\n".join(lines)
    print(table)
    print(f"\nwrote {path}")
    if summary := os.getenv("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as f:
            f.write(table + "\n")


if __name__ == "__main__":
    main()
