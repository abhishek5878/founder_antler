#!/usr/bin/env python3
"""
Apify (apimaestro) Full LinkedIn Sections Pipeline
=================================================

- Reads LinkedIn profile URLs from serpapi_linkedin_urls.json (or accepts a fallback list)
- Calls Apify actor apimaestro~linkedin-profile-full-sections-scraper via run-sync-get-dataset-items
  to fetch full profile sections (experience, education, certifications, location) and optional email
- Saves raw items and stealth-filtered items

Endpoint (OpenAPI provided):
POST https://api.apify.com/v2/acts/apimaestro~linkedin-profile-full-sections-scraper/run-sync-get-dataset-items?token=...
Body: { usernames: ["https://linkedin.com/in/...", ...], includeEmail: true }
"""

import os
import json
import math
import time
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_BASE = "https://api.apify.com/v2"
ACTOR_PATH = "acts/apimaestro~linkedin-profile-full-sections-scraper/run-sync-get-dataset-items"

if not APIFY_TOKEN:
    print("❌ APIFY_TOKEN not set in environment. Aborting.")
    raise SystemExit(1)

STEALTH_KEYWORDS = [
    "stealth", "building", "working on", "exploring", "pre-seed", "early stage", "incubating"
]

INPUT_URLS_FILE = "serpapi_linkedin_urls.json"
RAW_OUT = "apimaestro_full_sections_raw.json"
STEALTH_OUT = "apimaestro_full_sections_stealth.json"


def read_urls() -> List[str]:
    if os.path.exists(INPUT_URLS_FILE):
        with open(INPUT_URLS_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            return [u for u in data if isinstance(u, str) and "linkedin.com/in/" in u]
    # Fallback: empty list
    return []


def call_apimaestro(usernames: List[str], include_email: bool = True) -> List[Dict[str, Any]]:
    url = f"{APIFY_BASE}/{ACTOR_PATH}?token={APIFY_TOKEN}"
    payload = {"usernames": usernames, "includeEmail": include_email}
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return [{"raw": r.text}]


def looks_stealth(item: Dict[str, Any]) -> bool:
    text = " ".join(
        str(v) for v in [
            item.get("headline", ""), item.get("about", ""), item.get("summary", ""),
            item.get("experience", ""), item.get("experiences", ""), item.get("positions", ""),
            item.get("currentJobTitle", ""), item.get("currentCompany", ""),
        ]
    ).lower()
    return any(k in text for k in STEALTH_KEYWORDS)


def main():
    print("🚀 Apify apimaestro full sections pipeline")
    urls = read_urls()
    print(f"🔗 Input URLs: {len(urls)}")
    if not urls:
        print("❌ No URLs found in serpapi_linkedin_urls.json. Run SerpAPI discovery first.")
        return

    # Apimaestro supports up to 500 usernames per call per schema. We'll batch smaller (e.g., 50) to be safe.
    batch_size = 50
    all_items: List[Dict[str, Any]] = []

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        print(f"📦 Batch {i//batch_size + 1} — {len(batch)} profiles")
        try:
            items = call_apimaestro(batch, include_email=True)
            print(f"   ↳ Received {len(items)} items")
            all_items.extend(items if isinstance(items, list) else [items])
            time.sleep(1.5)
        except requests.HTTPError as e:
            print(f"   ↳ HTTPError: {e}")
            continue
        except Exception as e:
            print(f"   ↳ Error: {e}")
            continue

    # Save raw
    with open(RAW_OUT, "w") as f:
        json.dump(all_items, f, indent=2)
    print(f"🗂️ Saved raw items: {len(all_items)} -> {RAW_OUT}")

    # Filter stealth
    stealth_items = [it for it in all_items if isinstance(it, dict) and looks_stealth(it)]
    with open(STEALTH_OUT, "w") as f:
        json.dump(stealth_items, f, indent=2)
    print(f"🕵️ Stealth-matching: {len(stealth_items)} -> {STEALTH_OUT}")

    if stealth_items[:5]:
        print("\nTop stealth samples:")
        for i, it in enumerate(stealth_items[:5], 1):
            print(f"{i}. {it.get('profileUrl') or it.get('url') or it.get('publicIdentifier')} — {it.get('headline')}")


if __name__ == "__main__":
    main()
