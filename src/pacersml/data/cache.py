"""Caches. Raw API responses are stored as gzipped JSON exactly as received:
data/raw/{season}/{source}_{endpoint}/{game_id}.json.gz, and normalized on every load, so a parser fix never
needs a re-download. A game that is final never changes, so once cached it is never re-fetched.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
MANIFEST = DATA / "manifest.json"


def raw_path(season: str, key: str, game_id: str) -> Path:
    return RAW / season / key / f"{game_id}.json.gz"


def find_raw(season: str, keys: list[str], game_id: str) -> tuple[str, dict] | None:
    """First cached payload among `keys` (in preference order), as (key, payload)."""
    for key in keys:
        p = raw_path(season, key, game_id)
        if p.exists():
            with gzip.open(p, "rt", encoding="utf-8") as f:
                return key, json.load(f)
    return None


def write_raw(payload: dict, season: str, key: str, game_id: str) -> None:
    p = raw_path(season, key, game_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(p, "wt", encoding="utf-8") as f:
        json.dump(payload, f)


def write_processed(df: pd.DataFrame, name: str) -> Path:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    p = PROCESSED / f"{name}.parquet"
    df.to_parquet(p, index=False)
    return p


def frame_hash(df: pd.DataFrame) -> str:
    return hashlib.sha256(pd.util.hash_pandas_object(df, index=False).values.tobytes()).hexdigest()[:16]


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"seasons": {}}


def save_manifest(m: dict) -> None:
    DATA.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2, sort_keys=True))


def is_frozen(season: str) -> bool:
    return load_manifest()["seasons"].get(season, {}).get("frozen", False)
