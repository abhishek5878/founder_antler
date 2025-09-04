#!/usr/bin/env python3
"""
Apify Batch LinkedIn Scraper (No Cookies)
=========================================

Reads LinkedIn profile URLs from serpapi_linkedin_urls.json and calls:
POST /acts/apimaestro~linkedin-profile-batch-scraper-no-cookies-required/run-sync-get-dataset-items?token=...
with body { usernames: [...], includeEmail: true }
Saves combined results to apimaestro_batch_raw.json
"""

import os
import json
import time
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_BASE = "https://api.apify.com/v2"
ACTOR_PATH = "acts/apimaestro~linkedin-profile-batch-scraper-no-cookies-required/run-sync-get-dataset-items"
INPUT_URLS_FILE = "serpapi_linkedin_urls.json"
OUT_RAW = "apimaestro_batch_raw.json"

if not APIFY_TOKEN:
    print("❌ APIFY_TOKEN not set in environment. Aborting.")
    raise SystemExit(1)


def read_urls() -> List[str]:
    if not os.path.exists(INPUT_URLS_FILE):
        return []
    with open(INPUT_URLS_FILE, "r") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [u for u in data if isinstance(u, str) and "linkedin.com/in/" in u]
    return []


def call_actor(usernames: List[str], include_email: bool = True) -> List[Dict[str, Any]]:
    url = f"{APIFY_BASE}/{ACTOR_PATH}?token={APIFY_TOKEN}"
    payload = {"usernames": usernames, "includeEmail": include_email}
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return [{"raw": r.text}]


def main():
    urls = read_urls()
    print(f"🔗 Loaded {len(urls)} LinkedIn URLs")
    if not urls:
        print("❌ No URLs to process. Ensure serpapi_linkedin_urls.json exists.")
        return

    batch_size = 100  # actor supports up to 500; use 100 for reliability
    all_items: List[Dict[str, Any]] = []

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        print(f"📦 Batch {i//batch_size+1}: {len(batch)} profiles")
        try:
            items = call_actor(batch, include_email=True)
            print(f"   ↳ Received {len(items)} items")
            if isinstance(items, list):
                all_items.extend(items)
            else:
                all_items.append(items)
            time.sleep(1.0)
        except requests.HTTPError as e:
            print(f"   ↳ HTTPError: {e}")
            continue
        except Exception as e:
            print(f"   ↳ Error: {e}")
            continue

    with open(OUT_RAW, "w") as f:
        json.dump(all_items, f, indent=2)
    print(f"🗂️ Saved {len(all_items)} items -> {OUT_RAW}")


if __name__ == "__main__":
    main()
