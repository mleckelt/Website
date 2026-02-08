#!/usr/bin/env python3
"""
Simple scraper to fetch Google Scholar stats and write a small JSON file.

Usage:
  pip install requests beautifulsoup4
  python fetch_scholar_stats.py

The script writes `scholar_stats.json` next to this file.
"""
import json
import time
import requests
from bs4 import BeautifulSoup

# Set your Google Scholar profile URL (public profile)
SCHOLAR_URL = 'https://scholar.google.de/citations?user=arVjclEAAAAJ&hl=en'
OUT_FILE = 'static/scholar_stats.json'


def fetch_stats(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; stats-scraper/1.0; +https://example.org)'
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Google Scholar uses id="gsc_rsb_st" for the stats table; fall back to class if needed
    table = soup.find('table', id='gsc_rsb_st') or soup.find('table', class_='gsc_rsb_st')
    if not table:
        # Try a looser search: look for a table that contains a cell with text 'Citations'
        candidates = soup.find_all('table')
        for t in candidates:
            if t.find(string=lambda s: s and 'Citations' in s):
                table = t
                break

    if not table:
        # Save fetched HTML for debugging
        with open('scholar_profile_debug.html', 'w', encoding='utf-8') as fh:
            fh.write(resp.text)
        raise RuntimeError('Could not find stats table on the profile page; saved scholar_profile_debug.html')

    rows = table.find_all('tr')
    if len(rows) < 4:
        raise RuntimeError('Unexpected stats table structure')

    # Expect rows: header, citations, h-index, i10-index
    def td_text(row, idx=1):
        cols = row.find_all('td')
        if len(cols) > idx:
            return cols[idx].get_text(strip=True).replace('\xa0', ' ')
        return ''

    citations = td_text(rows[1])
    h_index = td_text(rows[2])
    h_index_10 = td_text(rows[3])

    return {
        'citations': citations,
        'h_index': h_index,
        'h_index_10': h_index_10,
        'fetched_at': int(time.time())
    }


def main():
    stats = fetch_stats(SCHOLAR_URL)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    print('Wrote', OUT_FILE)


if __name__ == '__main__':
    main()
