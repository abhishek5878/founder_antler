#!/usr/bin/env python3
"""
SerpAPI -> Apify LinkedIn Details Pipeline
=========================================

1) Use SerpAPI to search Google for stealth-founder queries (with pagination)
2) Extract LinkedIn profile URLs
3) Feed URLs into the provided Apify LinkedIn details TASK in batches
4) Save raw and stealth-filtered outputs
"""

import os
import time
import json
from typing import Any, Dict, List, Set

import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
LINKEDIN_TASK_ID = os.getenv("APIFY_LINKEDIN_TASK_ID", "eloquent_outlook~linkedin-profile-details-scraper")
APIFY_BASE = "https://api.apify.com/v2"

if not SERPAPI_KEY:
    print("❌ SERPAPI_KEY not set in environment. Aborting.")
    raise SystemExit(1)
if not APIFY_TOKEN:
    print("❌ APIFY_TOKEN not set in environment. Aborting.")
    raise SystemExit(1)

STEALTH_KEYWORDS = [
    "stealth", "building", "building something", "working on", "exploring",
    "pre-seed", "early stage", "incubating", "founder in stealth",
]

QUERIES = [
    'site:linkedin.com/in/ "building something" (founder OR co-founder)',
    'site:linkedin.com/in/ "stealth mode" (founder OR co-founder)',
    'site:linkedin.com/in/ "working on something" (founder OR co-founder)',
    'site:linkedin.com/in/ "exploring opportunities" (founder OR co-founder)',
    'site:linkedin.com/in/ (2024 OR 2023) (founder OR co-founder) (AI OR fintech OR healthtech)',
    'site:linkedin.com/in/ (ex-google OR ex-meta OR ex-amazon OR ex-microsoft OR ex-apple) building (founder OR co-founder)',
    'site:linkedin.com/in/ MBA (2024 OR 2023) (founder OR co-founder)',
    'site:linkedin.com/in/ (San Francisco OR New York OR London OR Singapore OR Bangalore) (stealth OR building) (founder OR co-founder)'
]

RESULTS_PER_PAGE = 10
PAGES_PER_QUERY = 5  # 5 pages * 8 queries * 10 ~= 400 candidates before de-dup


def serpapi_search(query: str, start: int = 0) -> Dict[str, Any]:
    params = {
        "engine": "google",
        "q": query,
        "num": RESULTS_PER_PAGE,
        "start": start,
        "hl": "en",
        "gl": "us",
        "api_key": SERPAPI_KEY,
    }
    r = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def extract_linkedin_urls_from_serp(result: Dict[str, Any]) -> Set[str]:
    urls: Set[str] = set()
    def add(url: str):
        if "linkedin.com/in/" in url:
            urls.add(url.split("?")[0].rstrip("/"))
    for item in result.get("organic_results", []) or []:
        link = item.get("link")
        if link:
            add(link)
        for sl in (item.get("sitelinks", {}).get("expanded", []) or []):
            if isinstance(sl, dict) and sl.get("link"):
                add(sl["link"])
    for k in ["inline_results", "related_searches", "news_results"]:
        for item in result.get(k, []) or []:
            link = item.get("link")
            if link:
                add(link)
    return urls


def run_task_with_urls(task_id: str, urls: List[str]) -> Dict[str, Any]:
    url = f"{APIFY_BASE}/actor-tasks/{task_id}/runs?token={APIFY_TOKEN}"
    payload = {"startUrls": [{"url": u} for u in urls]}
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()


def poll_run(run_id: str, interval_sec: float = 5.0, timeout_sec: int = 1200) -> Dict[str, Any]:
    url = f"{APIFY_BASE}/actor-runs/{run_id}?token={APIFY_TOKEN}"
    start = time.time()
    while True:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        status = data.get("data", {}).get("status")
        if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMING_OUT", "TIMED_OUT"}:
            return data
        if time.time() - start > timeout_sec:
            raise TimeoutError(f"Polling timed out for run {run_id}")
        time.sleep(interval_sec)


def fetch_dataset_items(dataset_id: str, limit: int = 5000) -> List[Dict[str, Any]]:
    url = f"{APIFY_BASE}/datasets/{dataset_id}/items?token={APIFY_TOKEN}&clean=true&limit={limit}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return [{"raw": r.text}]


def looks_stealthy_blob(item: Dict[str, Any]) -> bool:
    text = " ".join([
        str(item.get("headline", "")),
        str(item.get("about", "")),
        str(item.get("summary", "")),
        str(item.get("title", "")),
        str(item.get("positions", "")),
        str(item.get("experiences", "")),
    ]).lower()
    return any(k in text for k in STEALTH_KEYWORDS)


def main():
    print("🚀 SerpAPI -> Apify pipeline (expanded)")
    all_urls: Set[str] = set()

    for qi, q in enumerate(QUERIES, 1):
        for p in range(PAGES_PER_QUERY):
            start = p * RESULTS_PER_PAGE
            print(f"🔎 [{qi}/{len(QUERIES)}] page {p+1}/{PAGES_PER_QUERY}: {q[:70]}… (start={start})")
            try:
                res = serpapi_search(q, start=start)
                urls = extract_linkedin_urls_from_serp(res)
                print(f"   ↳ Found {len(urls)} URLs on this page")
                all_urls.update(urls)
                time.sleep(1.5)
            except Exception as e:
                print(f"   ↳ Error: {e}")
                continue

    urls_list = sorted(all_urls)
    print(f"🔗 Total unique LinkedIn URLs: {len(urls_list)}")
    with open("serpapi_linkedin_urls.json", "w") as f:
        json.dump(urls_list, f, indent=2)

    if not urls_list:
        print("❌ No URLs found. Consider increasing pages or adjusting queries.")
        return

    batch_size = 25
    all_items: List[Dict[str, Any]] = []

    for i in range(0, len(urls_list), batch_size):
        batch = urls_list[i:i+batch_size]
        print(f"📦 Running Apify LinkedIn details task for batch {i//batch_size+1} ({len(batch)} URLs)…")
        task_run = run_task_with_urls(LINKEDIN_TASK_ID, batch)
        run_id = task_run.get("data", {}).get("id")
        if not run_id:
            print("   ↳ Failed to start run")
            continue
        final_run = poll_run(run_id)
        status = final_run.get("data", {}).get("status")
        dataset_id = final_run.get("data", {}).get("defaultDatasetId")
        print(f"   ↳ Status: {status}")
        if dataset_id:
            items = fetch_dataset_items(dataset_id)
            all_items.extend(items)
        time.sleep(2)

    with open("serpapi_apify_linkedin_raw.json", "w") as f:
        json.dump(all_items, f, indent=2)
    print(f"🗂️ Aggregated {len(all_items)} LinkedIn items")

    stealth_items = [it for it in all_items if looks_stealthy_blob(it)]
    with open("serpapi_apify_linkedin_stealth.json", "w") as f:
        json.dump(stealth_items, f, indent=2)
    print(f"🕵️ Stealth-matching items: {len(stealth_items)}")

    print("\n✅ Outputs:")
    print("- serpapi_linkedin_urls.json (discovered LinkedIn URLs)")
    print("- serpapi_apify_linkedin_raw.json (Apify enriched items)")
    print("- serpapi_apify_linkedin_stealth.json (stealth-filtered)")


if __name__ == "__main__":
    main()
