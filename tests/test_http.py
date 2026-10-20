import pytest

from pacersml.data import http
from pacersml.data.http import Client, EndpointBlocked, EndpointError


class FakeResponse:
    def __init__(self, status):
        self.status_code = status
        self.url = "https://stats.nba.com/stats/gamerotation"

        class Elapsed:
            @staticmethod
            def total_seconds():
                return 0.3
        self.elapsed = Elapsed()

    def json(self):
        return {"ok": True}


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(http.time, "sleep", lambda s: None)
    c = Client(min_interval=0, retries=3, cooldown_after=2, cooldown_s=600)
    return c


def test_server_error_retries_then_falls_back_without_blocking_host(client, monkeypatch):
    calls = []
    monkeypatch.setattr(client.session, "get", lambda *a, **k: calls.append(1) or FakeResponse(500))
    with pytest.raises(EndpointError):
        client.stats("gamerotation", {})
    assert len(calls) == 3 and "stats.nba.com" not in client.blocked_hosts
    with pytest.raises(EndpointError):
        client.stats("gamerotation", {})
    assert "stats/gamerotation" in client.cooling_until            # 2 failed calls in a row
    with pytest.raises(EndpointError):
        client.stats("gamerotation", {})
    assert len(calls) == 6                                          # cooling down: no further requests
    client.cooling_until["stats/gamerotation"] = 0                  # cooldown over: tried again
    with pytest.raises(EndpointError):
        client.stats("gamerotation", {})
    assert len(calls) == 9


def test_retry_recovers_and_resets_streak(client, monkeypatch):
    seq = iter([500, 200, 500, 500, 500])
    monkeypatch.setattr(client.session, "get", lambda *a, **k: FakeResponse(next(seq)))
    assert client.stats("gamerotation", {}) == {"ok": True}
    with pytest.raises(EndpointError):
        client.stats("gamerotation", {})
    assert "stats/gamerotation" not in client.cooling_until         # streak restarted after the success


def test_refusal_blocks_host(client, monkeypatch):
    monkeypatch.setattr(client.session, "get", lambda *a, **k: FakeResponse(403))
    with pytest.raises(EndpointBlocked):
        client.cdn("liveData/playbyplay/playbyplay_0022500005.json")
    assert "cdn.nba.com" in client.blocked_hosts
