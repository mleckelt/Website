#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path

import requests

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
if not SERPAPI_KEY:
    raise RuntimeError("SERPAPI_KEY not set")

OUT_FILE = Path("static/scholar_stats.json")
TMP_FILE = OUT_FILE.with_suffix(".json.tmp")

SCHOLAR_ID = "arVjclEAAAAJ"


def fetch_stats():
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "api_key": SERPAPI_KEY,
    }

    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        print("SerpAPI error:", r.status_code, r.text[:500])
    r.raise_for_status()
    data = r.json()

    stats = {
        "citations": str(data["cited_by"]["table"][0]["citations"]["all"]),
        "h_index": str(data["cited_by"]["table"][1]["h_index"]["all"]),
        "h_index_10": str(data["cited_by"]["table"][2]["i10_index"]["all"]),
        "fetched_at": int(time.time()),
    }

    return stats


def atomic_write(data):
    TMP_FILE.parent.mkdir(parents=True, exist_ok=True)
    TMP_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    TMP_FILE.replace(OUT_FILE)


def main():
    try:
        stats = fetch_stats()
        atomic_write(stats)
        print("Updated", OUT_FILE)
    except Exception as e:
        print("ERROR:", e)
        if OUT_FILE.exists():
            print("Keeping existing file.")
        else:
            raise


if __name__ == "__main__":
    main()