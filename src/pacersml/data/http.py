"""Throttled HTTP access to stats.nba.com, cdn.nba.com and pbpstats.com.

stats.nba.com often hangs (rather than refusing) when it blocks an IP range, so repeated timeouts are
promoted to EndpointBlocked and the caller decides whether to fall back to another source.
"""
from __future__ import annotations

import random
import time

import requests

STATS_HEADERS = {
    "Host": "stats.nba.com",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Connection": "keep-alive",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}
CDN_HEADERS = {
    "User-Agent": STATS_HEADERS["User-Agent"],
    "Accept": "application/json",
    "Referer": "https://www.nba.com/",
}


class EndpointBlocked(RuntimeError):
    """Raised when a host times out or refuses repeatedly; treat the host as unavailable for this run."""


class Client:
    def __init__(self, timeout: float = 30.0, min_interval: float = 1.0, retries: int = 3):
        self.timeout = timeout
        self.min_interval = min_interval
        self.retries = retries
        self.session = requests.Session()
        self._last = 0.0
        self.blocked_hosts: set[str] = set()

    def _throttle(self) -> None:
        wait = self.min_interval + random.uniform(0, 0.4) - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None, host: str = "") -> dict:
        if host in self.blocked_hosts:
            raise EndpointBlocked(f"{host} already marked blocked this run")
        last_err: Exception | None = None
        for attempt in range(self.retries):
            self._throttle()
            try:
                r = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            except (requests.Timeout, requests.ConnectionError) as e:
                last_err = e
            else:
                if r.status_code == 200:
                    return r.json()
                if r.status_code == 404:
                    raise FileNotFoundError(f"404 {r.url}")
                last_err = RuntimeError(f"HTTP {r.status_code} {r.url}")
            time.sleep(2 ** attempt * 2)
        self.blocked_hosts.add(host)
        raise EndpointBlocked(f"{host}: {last_err}")

    def stats(self, endpoint: str, params: dict) -> dict:
        return self.get_json(f"https://stats.nba.com/stats/{endpoint}", params, STATS_HEADERS, "stats.nba.com")

    def cdn(self, path: str) -> dict:
        return self.get_json(f"https://cdn.nba.com/static/json/{path}", None, CDN_HEADERS, "cdn.nba.com")
