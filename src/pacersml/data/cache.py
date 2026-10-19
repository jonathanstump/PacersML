"""Parquet cache for raw per-game pulls: data/raw/{season}/{endpoint}/{game_id}.parquet.

A game that is final never changes, so once cached it is never re-fetched.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
MANIFEST = DATA / "manifest.json"


def raw_path(season: str, endpoint: str, game_id: str) -> Path:
    return RAW / season / endpoint / f"{game_id}.parquet"


def has_raw(season: str, endpoint: str, game_id: str) -> bool:
    return raw_path(season, endpoint, game_id).exists()


def read_raw(season: str, endpoint: str, game_id: str) -> pd.DataFrame:
    return pd.read_parquet(raw_path(season, endpoint, game_id))


def write_raw(df: pd.DataFrame, season: str, endpoint: str, game_id: str) -> None:
    p = raw_path(season, endpoint, game_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(p, index=False)


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
