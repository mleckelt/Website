#!/usr/bin/env python3
"""
Scraper to fetch Google Scholar stats and write a small JSON file.

Hardening:
- Polite scraping: jitter + retries + backoff
- Fail-safe writes: only replace JSON if scrape+parse+validation succeeds
- Keeps last-known-good JSON if anything goes wrong
"""
import json
import time
import random
import re
import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

SCHOLAR_URL = "https://scholar.google.de/citations?user=arVjclEAAAAJ&hl=en"
OUT_FILE = Path("static/scholar_stats.json")
TMP_FILE = OUT_FILE.with_suffix(OUT_FILE.suffix + ".tmp")
DEBUG_HTML = Path("scholar_profile_debug.html")

# --- polite HTTP session with retries + backoff ---
_session = requests.Session()
_retries = Retry(
    total=5,
    backoff_factor=1.0,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
_session.mount("https://", HTTPAdapter(max_retries=_retries))
_session.mount("http://", HTTPAdapter(max_retries=_retries))

HEADERS = {
    "User-Agent": (
        "mleckelt-scholar-stats-bot/1.0 "
        "(+https://mleckelt.github.io/Website/#home; contact: aaihjblkc@mozmail.com)"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _normalize_number_text(s: str) -> str:
    if s is None:
        return ""
    s = s.strip().replace("\xa0", " ")
    s = s.replace(" ", "")
    return s


def _looks_like_number(s: str) -> bool:
    if not s:
        return False
    # digits with optional thousands separators, e.g. 1234 or 1,234
    return re.fullmatch(r"\d{1,3}(?:,\d{3})*|\d+", s) is not None


def fetch_stats(url: str) -> dict:
    # polite delay with jitter
    time.sleep(1.0 + random.random() * 1.5)

    resp = _session.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    table = soup.find("table", id="gsc_rsb_st") or soup.find("table", class_="gsc_rsb_st")
    if not table:
        for t in soup.find_all("table"):
            if t.find(string=lambda s: s and "Citations" in s):
                table = t
                break

    if not table:
        DEBUG_HTML.write_text(resp.text, encoding="utf-8")
        raise RuntimeError("Could not find stats table; saved scholar_profile_debug.html")

    rows = table.find_all("tr")
    if len(rows) < 4:
        DEBUG_HTML.write_text(resp.text, encoding="utf-8")
        raise RuntimeError("Unexpected stats table structure; saved scholar_profile_debug.html")

    def td_text(row, idx=1) -> str:
        cols = row.find_all("td")
        if len(cols) > idx:
            return _normalize_number_text(cols[idx].get_text(strip=True))
        return ""

    citations = td_text(rows[1])
    h_index = td_text(rows[2])
    h_index_10 = td_text(rows[3])

    stats = {
        "citations": citations,
        "h_index": h_index,
        "h_index_10": h_index_10,
        "fetched_at": int(time.time()),
    }

    # Validate: blocked pages / markup shifts often yield empty/non-numeric fields
    if not (_looks_like_number(citations) and _looks_like_number(h_index) and _looks_like_number(h_index_10)):
        DEBUG_HTML.write_text(resp.text, encoding="utf-8")
        raise RuntimeError(
            f"Unexpected values (possible block/markup change): {stats}. "
            "Saved scholar_profile_debug.html"
        )

    return stats


def _read_existing_stats() -> dict | None:
    if OUT_FILE.exists():
        try:
            return json.loads(OUT_FILE.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def _atomic_write_json(path: Path, tmp_path: Path, data: dict) -> None:
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp_path, path)  # atomic replacement


def main() -> int:
    existing = _read_existing_stats()

    try:
        stats = fetch_stats(SCHOLAR_URL)
        _atomic_write_json(OUT_FILE, TMP_FILE, stats)
        print("Wrote", OUT_FILE)
        return 0

    except Exception as e:
        print("ERROR:", e)
        if existing is not None:
            print("Keeping existing", OUT_FILE, "(last-known-good).")
        else:
            print("No existing stats file to keep.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())