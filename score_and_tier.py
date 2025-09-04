#!/usr/bin/env python3
"""
Score and Tier LinkedIn Profiles
================================

Reads enriched items from Apify (apimaestro_full_sections_raw.json preferred,
else serpapi_apify_linkedin_raw.json), computes a stealth-fit score using
weights aligned with our stealth scoring system, and assigns Tier A/B/C.

Outputs:
- scored_profiles.json
- scored_profiles.csv
- scored_summary.json (counts per tier)
"""

import os
import json
import csv
from typing import Any, Dict, List

PREFERRED_INPUT = "apimaestro_full_sections_raw.json"
FALLBACK_INPUT = "serpapi_apify_linkedin_raw.json"
OUT_JSON = "scored_profiles.json"
OUT_CSV = "scored_profiles.csv"
OUT_SUMMARY = "scored_summary.json"

STEALTH_TERMS = ["stealth", "building", "working on", "exploring", "incubating", "pre-seed", "early stage"]
RECENT_TERMS = ["2024", "2023", "recent", "new"]
TOP_BG_TERMS = [
    "stanford", "harvard", "mit", "berkeley", "oxford", "cambridge",
    "google", "meta", "facebook", "amazon", "microsoft", "apple", "stripe", "airbnb", "tesla"
]
AI_TERMS = ["ai", "machine learning", "ml", "deep learning"]
FIN_TERMS = ["fintech", "payments", "banking", "crypto", "defi"]
HEALTH_TERMS = ["healthtech", "health", "biotech", "medical", "clinical"]
GEO_TERMS = [
    "san francisco", "new york", "london", "singapore", "bangalore", "berlin", "stockholm", "paris", "sydney"
]
NETWORK_TERMS = ["yc", "y combinator", "techstars", "500 startups", "antler", "accelerator", "alumni"]
CONV_TERMS = ["building", "exploring", "looking for", "hiring", "open to", "seeking"]


def normalize_text(*parts: Any) -> str:
    return " ".join([str(p) for p in parts if p is not None]).lower()


def score_item(item: Dict[str, Any]) -> Dict[str, Any]:
    url = item.get("profileUrl") or item.get("url") or item.get("publicIdentifier") or ""
    headline = item.get("headline") or item.get("title") or ""
    about = item.get("about") or item.get("summary") or ""
    experiences = item.get("positions") or item.get("experiences") or []
    experience_blob = " ".join(
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
    text = normalize_text(url, headline, about, experience_blob)

    # Subscores
    stealth_score = sum(1 for t in STEALTH_TERMS if t in text)  # 0..N
    recent_score = sum(1 for t in RECENT_TERMS if t in text)
    background_score = sum(1 for t in TOP_BG_TERMS if t in text)

    industry_score = 0
    if any(t in text for t in AI_TERMS):
        industry_score += 2
    if any(t in text for t in FIN_TERMS):
        industry_score += 2
    if any(t in text for t in HEALTH_TERMS):
        industry_score += 2

    geo_score = sum(1 for t in GEO_TERMS if t in text)
    network_score = sum(1 for t in NETWORK_TERMS if t in text)
    conv_score = sum(1 for t in CONV_TERMS if t in text)

    # Weighted total (align with earlier weighting)
    total = (
        stealth_score * 0.25 +
        recent_score * 0.20 +
        background_score * 0.15 +
        industry_score * 0.15 +
        geo_score * 0.10 +
        network_score * 0.10 +
        conv_score * 0.05
    )

    # Normalize to 0-10 range with cap
    total = min(10.0, round(total, 2))

    if total >= 7.5:
        tier = "A"
    elif total >= 6.0:
        tier = "B"
    else:
        tier = "C"

    return {
        "url": url,
        "headline": headline,
        "about": about,
        "score": total,
        "tier": tier,
    }


def read_input_items() -> List[Dict[str, Any]]:
    path = PREFERRED_INPUT if os.path.exists(PREFERRED_INPUT) else FALLBACK_INPUT
    if not os.path.exists(path):
        print(f"❌ No input file found. Expected {PREFERRED_INPUT} or {FALLBACK_INPUT}.")
        return []
    with open(path, "r") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception:
            return []
    return []


def main():
    items = read_input_items()
    print(f"📥 Loaded {len(items)} enriched items")
    if not items:
        return

    scored: List[Dict[str, Any]] = [score_item(it) for it in items]

    # Save JSON
    with open(OUT_JSON, "w") as f:
        json.dump(scored, f, indent=2)

    # Save CSV
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "headline", "score", "tier"])
        for r in scored:
            w.writerow([r.get("url", ""), r.get("headline", ""), r.get("score", 0), r.get("tier", "")])

    # Summary
    summary = {"A": 0, "B": 0, "C": 0}
    for r in scored:
        t = r.get("tier")
        if t in summary:
            summary[t] += 1
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Scored {len(scored)} profiles")
    print(f"🏷️ Tiers: A={summary['A']} | B={summary['B']} | C={summary['C']}")
    print(f"📄 Outputs: {OUT_JSON}, {OUT_CSV}, {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
