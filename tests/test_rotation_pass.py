import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import rotation_pass as rp  # noqa: E402

from pacersml.data import cache  # noqa: E402
from pacersml.data.http import EndpointError  # noqa: E402

SEASON = "1999-00"
GIDS = [f"00299000{i:02d}" for i in range(6)]
CANARY = "0029900099"


def setup(tmp_path, monkeypatch, answers):
    """answers(gid, call_number) -> True (200) or False (failure)."""
    monkeypatch.setattr(cache, "RAW", tmp_path)
    for g in GIDS:
        p = cache.raw_path(SEASON, "stats_box", g)
        p.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(p, "wt") as f:
            json.dump({}, f)
    cache.write_raw({}, SEASON, "stats_rotation", CANARY)
    calls = []

    def stats(self, endpoint, params, **kw):
        gid = params["GameID"]
        calls.append(gid)
        if answers(gid, len(calls)):
            return {"ok": True}
        raise EndpointError("timeout")
    monkeypatch.setattr(rp.Client, "stats", stats)
    monkeypatch.setattr(rp.time, "sleep", lambda s: None)
    monkeypatch.setattr(sys, "argv", ["rotation_pass", "--seasons", SEASON, "--interval", "0"])
    return calls


def ledger():
    p = cache.RAW / SEASON / "rotation_attempts.json"
    return json.loads(p.read_text()) if p.exists() else {}


def test_throttled_failures_are_not_counted_and_the_game_is_retried(tmp_path, monkeypatch):
    # calls 1-2: the first game and the canary both fail (throttled); everything answers afterwards
    calls = setup(tmp_path, monkeypatch, lambda gid, n: n > 2)
    assert rp.main() == 0
    assert calls[:3] == [GIDS[0], CANARY, GIDS[0]]
    assert all(v == 0 for v in ledger().values())
    assert len(list((tmp_path / SEASON / "stats_rotation").glob("*.json.gz"))) == len(GIDS) + 1


def test_game_failure_counts_when_canary_answers_and_gets_a_second_round(tmp_path, monkeypatch):
    # GIDS[1] fails on its first try only; the canary always answers
    seen = {}

    def answers(gid, n):
        seen[gid] = seen.get(gid, 0) + 1
        return gid != GIDS[1] or seen[gid] > 1
    setup(tmp_path, monkeypatch, answers)
    assert rp.main() == 0
    assert ledger() == {GIDS[1]: 1}
    assert rp.cache.find_raw(SEASON, ["stats_rotation"], GIDS[1]) is not None


def test_stops_after_all_backoffs(tmp_path, monkeypatch):
    setup(tmp_path, monkeypatch, lambda gid, n: False)
    assert rp.main() == 3
    assert all(v == 0 for v in ledger().values())
