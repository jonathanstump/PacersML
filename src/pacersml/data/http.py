"""Throttled HTTP access to stats.nba.com, cdn.nba.com and pbpstats.com.

stats.nba.com often hangs (rather than refusing) when it blocks an IP range, so repeated timeouts are
promoted to EndpointBlocked and the caller decides whether to fall back to another source.
"""
from __future__ import annotations

import random
import time

import requests

# The sec-ch-ua / sec-fetch-* headers are what NBA's CDN (Akamai) checks: without them both hosts refused us
# from every network tested (403 / hang), with them they answer (verified 2026-10-20). Keep them.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="141", "Chromium";v="141", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}
STATS_HEADERS = {**BROWSER_HEADERS, "Host": "stats.nba.com",
                 "x-nba-stats-origin": "stats", "x-nba-stats-token": "true"}
CDN_HEADERS = BROWSER_HEADERS


class EndpointBlocked(RuntimeError):
    """A host timed out or refused on every try of a call. The host is marked down; the caller (refresh.py)
    pauses, re-probes, and either clears `blocked_hosts` and continues or stops the run (D11)."""


class EndpointError(RuntimeError):
    """The host answers but this endpoint keeps returning server errors (gamerotation fails intermittently per
    game). Each call retries with backoff first (D10). After `cooldown_after` failed calls in a row the endpoint
    is skipped for `cooldown_s` seconds, then tried again; games that missed it get a second pass (D11)."""


class Client:
    # 1.5-2.0 s between requests (D10): a working fingerprint gets banned by pulling fast, not by pulling.
    def __init__(self, timeout: float = 30.0, min_interval: float = 1.5, retries: int = 3,
                 cooldown_after: int = 5, cooldown_s: float = 600.0):
        self.timeout = timeout
        self.min_interval = min_interval
        self.retries = retries
        self.cooldown_after = cooldown_after
        self.cooldown_s = cooldown_s
        self.session = requests.Session()
        self._last = 0.0
        self.blocked_hosts: set[str] = set()
        self.cooling_until: dict[str, float] = {}
        self._server_errors: dict[str, int] = {}

    def _throttle(self) -> None:
        wait = self.min_interval + random.uniform(0, 0.5) - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None, host: str = "",
                 endpoint: str = "", backoff: float = 2.0) -> dict:
        endpoint = endpoint or url
        if host in self.blocked_hosts:
            raise EndpointBlocked(f"{host} marked down")
        if time.monotonic() < self.cooling_until.get(endpoint, 0):
            raise EndpointError(f"{endpoint} cooling down after repeated server errors")
        last_err: Exception | None = None
        server_error = False
        for attempt in range(self.retries):
            self._throttle()
            try:
                r = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            except (requests.Timeout, requests.ConnectionError) as e:
                last_err, server_error = e, False
            else:
                if r.status_code == 200:
                    self._server_errors[endpoint] = 0
                    return r.json()
                if r.status_code == 404:
                    raise FileNotFoundError(f"404 {r.url}")
                # a fast 5xx is the endpoint failing, not the host blocking us
                server_error = r.status_code >= 500 and r.elapsed.total_seconds() < self.timeout
                last_err = RuntimeError(f"HTTP {r.status_code} {r.url}")
            if attempt + 1 < self.retries:
                time.sleep(backoff * 2 ** attempt)
        if server_error:
            n = self._server_errors.get(endpoint, 0) + 1
            self._server_errors[endpoint] = n
            if n >= self.cooldown_after:
                self.cooling_until[endpoint] = time.monotonic() + self.cooldown_s
                self._server_errors[endpoint] = 0
            raise EndpointError(f"{endpoint}: {last_err} after {self.retries} tries ({n} calls in a row)")
        self.blocked_hosts.add(host)
        raise EndpointBlocked(f"{host}: {last_err}")

    def stats(self, endpoint: str, params: dict, backoff: float = 2.0) -> dict:
        return self.get_json(f"https://stats.nba.com/stats/{endpoint}", params, STATS_HEADERS, "stats.nba.com",
                             f"stats/{endpoint}", backoff)

    def cdn(self, path: str) -> dict:
        # endpoint key drops the game id: liveData/boxscore/boxscore_0022500005.json -> cdn/liveData/boxscore/boxscore
        return self.get_json(f"https://cdn.nba.com/static/json/{path}", None, CDN_HEADERS, "cdn.nba.com",
                             "cdn/" + path.rsplit("_", 1)[0])
