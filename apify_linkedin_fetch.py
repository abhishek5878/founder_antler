#!/usr/bin/env python3
"""
Apify LinkedIn Profile Fetcher
==============================

Uses the provided Apify Actor Task endpoint to:
- Trigger a run
- Poll until completion
- Download dataset items
- Filter for stealth/early-stage founders

References:
- Run task endpoint: https://api.apify.com/v2/actor-tasks/{taskId}/runs
- Example provided by user: https://api.apify.com/v2/actor-tasks/eloquent_outlook~linkedin-profile-details-scraper/runs?token=...
"""

import os
import sys
import time
import json
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TASK_ID = os.getenv("APIFY_TASK_ID", "eloquent_outlook~linkedin-profile-details-scraper")
APIFY_BASE = "https://api.apify.com/v2"

if not APIFY_TOKEN:
    print("❌ APIFY_TOKEN not set in environment. Aborting.")
    sys.exit(1)

# Seed URLs (5 sample profiles); you can pass a file path via CLI to override
SEED_LINKEDIN_URLS = [
    "https://www.linkedin.com/in/anubhab/",
    "https://www.linkedin.com/in/tejasvi-ravi-082b352b/",
    "https://www.linkedin.com/in/sonia-vora-4b321377/",
    "https://www.linkedin.com/in/sanjeevsrinivasan07/",
    "https://www.linkedin.com/in/pskumar2018/",
]

STEALTH_KEYWORDS = [
    "stealth", "building", "building something", "working on", "exploring",
    "pre-seed", "early stage", "incubating", "founder in stealth",
]


def start_task_run(override_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{APIFY_BASE}/actor-tasks/{TASK_ID}/runs?token={APIFY_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = override_input or {}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def poll_run(run_id: str, interval_sec: float = 5.0, timeout_sec: int = 600) -> Dict[str, Any]:
    url = f"{APIFY_BASE}/actor-runs/{run_id}?token={APIFY_TOKEN}"
    start = time.time()
    while True:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("data", {}).get("status")
        if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMING_OUT", "TIMED_OUT"}:
            return data
        if time.time() - start > timeout_sec:
            raise TimeoutError(f"Polling timed out for run {run_id}")
        time.sleep(interval_sec)


def fetch_dataset_items(dataset_id: str, clean: bool = True, limit: int = 10000) -> List[Dict[str, Any]]:
    url = f"{APIFY_BASE}/datasets/{dataset_id}/items?token={APIFY_TOKEN}&clean={'true' if clean else 'false'}&limit={limit}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    try:
        return resp.json()
    except Exception:
        # If the actor produced CSV, NDJSON, etc., we return raw text as a single item
        return [{"raw": resp.text}]


def load_seed_urls_from_file(path: str) -> List[str]:
    with open(path, "r") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "urls" in data and isinstance(data["urls"], list):
        return data["urls"]
    raise ValueError("Unsupported seed file format. Provide a JSON list of URLs or {\"urls\": [...]}.")


def looks_stealthy(text: str) -> bool:
    text_l = (text or "").lower()
    return any(k in text_l for k in STEALTH_KEYWORDS)


def filter_stealth_profiles(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for it in items:
        url = it.get("url") or it.get("publicIdentifier") or it.get("profileUrl") or ""
        headline = it.get("headline") or it.get("title") or it.get("summary") or ""
        about = it.get("about") or it.get("description") or ""
        experiences = it.get("positions") or it.get("experiences") or []
        exp_text = " ".join(
            [
                " ".join(
                    str(v) for v in (
                        (exp.get("title") if isinstance(exp, dict) else None),
                        (exp.get("companyName") if isinstance(exp, dict) else None),
                        (exp.get("description") if isinstance(exp, dict) else None),
                    )
                )
                for exp in experiences if isinstance(exp, dict)
            ]
        )
        blob = " ".join([url, headline, about, exp_text])
        if looks_stealthy(blob):
            filtered.append({
                "url": url,
                "headline": headline,
                "about": about,
                "raw": it,
            })
    return filtered


def main():
    # Optional: allow providing a JSON file with seed LinkedIn URLs
    override_input_path = None
    if len(sys.argv) > 1:
        override_input_path = sys.argv[1]

    override_input: Optional[Dict[str, Any]] = None
    try:
        seed_urls = load_seed_urls_from_file(override_input_path) if override_input_path else SEED_LINKEDIN_URLS
        # Many Apify tasks accept input like { startUrls: [{ url: ... }, ...] }
        override_input = {
            "startUrls": [{"url": u} for u in seed_urls]
        }
    except Exception:
        # Fallback to no override (use task's default input)
        override_input = None

    print("🚀 Starting Apify task run…")
    run_resp = start_task_run(override_input)
    run_id = run_resp.get("data", {}).get("id")
    if not run_id:
        print("❌ Failed to start run:", json.dumps(run_resp, indent=2))
        sys.exit(1)

    print(f"⏳ Polling run status: {run_id}")
    final_run = poll_run(run_id)
    run_status = final_run.get("data", {}).get("status")
    dataset_id = final_run.get("data", {}).get("defaultDatasetId")

    print(f"🏁 Run finished with status: {run_status}")
    if not dataset_id:
        print("❌ No dataset produced. Full run data:")
        print(json.dumps(final_run, indent=2))
        sys.exit(1)

    print(f"📥 Downloading dataset items from: {dataset_id}")
    items = fetch_dataset_items(dataset_id)

    # Save raw items
    with open("apify_linkedin_raw.json", "w") as f:
        json.dump(items, f, indent=2)

    # Filter stealth/early-stage
    stealth_items = filter_stealth_profiles(items)
    with open("apify_stealth_founders.json", "w") as f:
        json.dump(stealth_items, f, indent=2)

    print(f"📊 Total items: {len(items)} | Stealth-matching: {len(stealth_items)}")
    if stealth_items[:5]:
        print("\nTop matches:")
        for i, it in enumerate(stealth_items[:5], 1):
            print(f"{i}. {it.get('url')} — {it.get('headline')}")

    print("\n✅ Files saved:")
    print("- apify_linkedin_raw.json (all scraped items)")
    print("- apify_stealth_founders.json (filtered stealth candidates)")


if __name__ == "__main__":
    main()
