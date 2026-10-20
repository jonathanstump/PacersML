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
    """Raised when a host times out or refuses repeatedly; treat the host as unavailable for this run."""


class EndpointError(RuntimeError):
    """The host answers but this endpoint returns server errors (e.g. gamerotation's 500 since 2026-10-20).
    The host stays usable; after `disable_after` consecutive failures the endpoint is skipped for the run."""


class Client:
    def __init__(self, timeout: float = 30.0, min_interval: float = 1.0, retries: int = 3, disable_after: int = 3):
        self.timeout = timeout
        self.min_interval = min_interval
        self.retries = retries
        self.disable_after = disable_after
        self.session = requests.Session()
        self._last = 0.0
        self.blocked_hosts: set[str] = set()
        self.disabled_endpoints: set[str] = set()
        self._server_errors: dict[str, int] = {}

    def _throttle(self) -> None:
        wait = self.min_interval + random.uniform(0, 0.4) - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None, host: str = "",
                 endpoint: str = "") -> dict:
        endpoint = endpoint or url
        if host in self.blocked_hosts:
            raise EndpointBlocked(f"{host} already marked blocked this run")
        if endpoint in self.disabled_endpoints:
            raise EndpointError(f"{endpoint} disabled this run after repeated server errors")
        last_err: Exception | None = None
        for attempt in range(self.retries):
            self._throttle()
            try:
                r = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            except (requests.Timeout, requests.ConnectionError) as e:
                last_err = e
            else:
                if r.status_code == 200:
                    self._server_errors[endpoint] = 0
                    return r.json()
                if r.status_code == 404:
                    raise FileNotFoundError(f"404 {r.url}")
                if r.status_code >= 500 and r.elapsed.total_seconds() < self.timeout:
                    # A fast 5xx is the endpoint failing, not the host blocking us: one try, no backoff.
                    n = self._server_errors.get(endpoint, 0) + 1
                    self._server_errors[endpoint] = n
                    if n >= self.disable_after:
                        self.disabled_endpoints.add(endpoint)
                    raise EndpointError(f"HTTP {r.status_code} {endpoint} ({n} in a row)")
                last_err = RuntimeError(f"HTTP {r.status_code} {r.url}")
            time.sleep(2 ** attempt * 2)
        self.blocked_hosts.add(host)
        raise EndpointBlocked(f"{host}: {last_err}")

    def stats(self, endpoint: str, params: dict) -> dict:
        return self.get_json(f"https://stats.nba.com/stats/{endpoint}", params, STATS_HEADERS, "stats.nba.com",
                             f"stats/{endpoint}")

    def cdn(self, path: str) -> dict:
        # endpoint key drops the game id: liveData/boxscore/boxscore_0022500005.json -> cdn/liveData/boxscore/boxscore
        return self.get_json(f"https://cdn.nba.com/static/json/{path}", None, CDN_HEADERS, "cdn.nba.com",
                             "cdn/" + path.rsplit("_", 1)[0])
