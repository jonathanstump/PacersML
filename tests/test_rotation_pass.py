import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import rotation_pass as rp  # noqa: E402

from pacersml.data import cache  # noqa: E402
from pacersml.data.http import EndpointError  # noqa: E402

SEASON = "1999-00"
GIDS = [f"00299000{i:02d}" for i in range(12)]


def setup(tmp_path, monkeypatch, outcomes, host):
    monkeypatch.setattr(cache, "RAW", tmp_path)
    for g in GIDS:
        p = cache.raw_path(SEASON, "stats_box", g)
        p.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(p, "wt") as f:
            json.dump({}, f)
    calls = []

    def stats(self, endpoint, params, **kw):
        calls.append(params["GameID"])
        self.n_requests += 1
        if next(outcomes):
            return {"ok": True}
        raise EndpointError("timeout")
    monkeypatch.setattr(rp.Client, "stats", stats)
    monkeypatch.setattr(rp, "host_up", lambda gid: next(host))
    monkeypatch.setattr(rp.time, "sleep", lambda s: None)
    monkeypatch.setattr(sys, "argv", ["rotation_pass", "--seasons", SEASON])
    return calls


def ledger():
    return json.loads((cache.RAW / SEASON / "rotation_attempts.json").read_text())


def test_outage_tries_are_taken_back_and_redone(tmp_path, monkeypatch):
    outcomes = iter([False] * 10 + [True] * 12)        # 10 timeouts during an outage, then everything answers
    calls = setup(tmp_path, monkeypatch, outcomes, iter([False]))
    assert rp.main() == 0
    assert calls[:10] == GIDS[:10] and calls[10:] == GIDS          # the 10 are redone after the pause
    assert all(v == 0 for v in ledger().values())
    assert len(list((tmp_path / SEASON / "stats_rotation").glob("*.json.gz"))) == 12


def test_real_rotation_failures_count_and_get_a_second_round(tmp_path, monkeypatch):
    outcomes = iter([False] * 12 + [False] * 2 + [True] * 10)  # host up; round 2 recovers 10 of 12
    calls = setup(tmp_path, monkeypatch, outcomes, iter([True, True]))
    assert rp.main() == 0
    assert len(calls) == 24
    led = ledger()
    assert sorted(led.values()) == [1] * 10 + [2] * 2           # two games used both tries
