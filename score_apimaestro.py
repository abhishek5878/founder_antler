#!/usr/bin/env python3
"""
Apimaestro Profile Scoring & Tiering (refined 100-point scheme)
===============================================================

Combines inputs:
- apimaestro_full_sections_stealth.json (if present)
- apimaestro_batch_raw.json (fallback/union)

De-duplicates by URL/public_identifier and scores all profiles.

Outputs:
- apimaestro_scored.json
- apimaestro_scored.csv
- apimaestro_scored_summary.json
- apimaestro_scored_tierA.csv (A only)
- apimaestro_scored_tierB.csv (B only)
"""

import os
import json
import csv
import re
from typing import Any, Dict, List, Tuple

INPUT_PREF = "apimaestro_full_sections_stealth.json"
INPUT_FALLBACK = "apimaestro_batch_raw.json"
OUT_JSON = "apimaestro_scored.json"
OUT_CSV = "apimaestro_scored.csv"
OUT_SUMMARY = "apimaestro_scored_summary.json"
OUT_A = "apimaestro_scored_tierA.csv"
OUT_B = "apimaestro_scored_tierB.csv"

# Terms (lowercased matching)
STEALTH_TERMS = ["stealth", "building", "working on", "exploring", "incubating", "in stealth"]
RECENT_YEARS = {2024, 2023}
FOUNDER_VARIANTS = ["founder", "co-founder", "cofounder", "co founder", "entrepreneur"]
TOP_SCHOOL_ALIASES = [
    "stanford", "harvard", "mit", "massachusetts institute of technology", "berkeley", "u.c. berkeley",
    "oxford", "cambridge", "wharton", "indian institute of technology", "iit ", "indian institute of management", "iim "
]
TOP_COMPANY_ALIASES = [
    "google", "google llc", "alphabet", "meta", "facebook", "amazon", "amazon.com", "microsoft", "microsoft corp",
    "apple", "apple inc", "stripe", "airbnb", "tesla", "openai"
]
AI_TERMS = [" genai", " ai ", " machine learning", " ml ", " deep learning", " nlp", " llm ", " computer vision", " mlops"]
FIN_TERMS = ["fintech", "payments", "payment", "banking", "lending", "issuer", "neobank", "crypto", "defi"]
HEALTH_TERMS = ["healthtech", " health ", "biotech", "medical", "clinical", "medtech", "digital health", "fda", "hl7"]
GEO_TERMS = ["san francisco", "bay area", "new york", "london", "singapore", "bangalore", "berlin", "stockholm", "paris", "sydney"]
ACCEL_TERMS = ["yc", "y combinator", "techstars", "500 startups", "antler", "accelerator", "cohort", "batch"]
OUTREACH_TERMS = ["hiring", "open to", "seeking", "building", "looking for"]

EXEC_BIGCO_TERMS = ["ceo", "chief executive officer", "cfo", "coo", "cto", "vp ", "vice president", "director", "head of"]

def to_text(*parts: Any) -> str:
    text = " ".join([str(p) for p in parts if p])
    text = re.sub(r"[\s\t\n]+", " ", text)
    return f" {text.strip().lower()} "

def mk_url(public_id: str) -> str:
    if not public_id:
        return ""
    return public_id if public_id.startswith("http") else f"https://www.linkedin.com/in/{public_id}"

def dedupe_profiles(list_a: List[Dict[str, Any]], list_b: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def key_of(p: Dict[str, Any]) -> Tuple[str]:
        basic = p.get("basic_info", {}) if isinstance(p, dict) else {}
        pid = (basic.get("public_identifier") or basic.get("profileUrl") or "").strip().lower()
        return (pid,)
    seen = set()
    out: List[Dict[str, Any]] = []
    for lst in (list_a, list_b):
        for p in lst or []:
            k = key_of(p)
            if not k[0]:
                # try to infer from nested
                pass
            if k in seen:
                continue
            seen.add(k)
            out.append(p)
    return out

def score_profile(p: Dict[str, Any]) -> Dict[str, Any]:
    basic = p.get("basic_info", {}) if isinstance(p, dict) else {}
    fullname = basic.get("fullname") or ""
    headline = basic.get("headline") or ""
    about = basic.get("about") or ""
    location = basic.get("location", {})
    loc_text = to_text(location.get("full"), location.get("city"), location.get("country"))
    email = basic.get("email")
    public_id = basic.get("public_identifier") or basic.get("profileUrl") or ""
    profile_url = mk_url(public_id)
    follower_count = basic.get("follower_count") or 0

    experiences = p.get("experience", []) if isinstance(p.get("experience"), list) else []

    blob_head = to_text(fullname, headline, about, loc_text)
    blob_exp_parts: List[str] = []

    current_recent = 0
    ended_recent = 0
    founder_hits = 0
    industry_ai = False
    industry_fin = False
    industry_health = False
    bg_company = False
    bg_school = False
    bigco_exec_flag = False

    for exp in experiences:
        title = to_text(exp.get("title"))
        company = to_text(exp.get("company"))
        blob_exp_parts.extend([title, company])

        if exp.get("is_current"):
            sy = exp.get("start_date", {}).get("year")
            if sy in RECENT_YEARS:
                current_recent += 1
        ey = exp.get("end_date", {}).get("year")
        if ey in RECENT_YEARS:
            ended_recent += 1

        if any(t in title for t in FOUNDER_VARIANTS):
            founder_hits += 1

        if any(t in title or t in company for t in AI_TERMS):
            industry_ai = True
        if any(t in title or t in company for t in FIN_TERMS):
            industry_fin = True
        if any(t in title or t in company for t in HEALTH_TERMS):
            industry_health = True

        if any(c in company for c in TOP_COMPANY_ALIASES):
            bg_company = True

        if any(k in title for k in EXEC_BIGCO_TERMS) and any(c in company for c in TOP_COMPANY_ALIASES):
            bigco_exec_flag = True

    education = p.get("education", []) if isinstance(p.get("education"), list) else []
    for ed in education:
        school = to_text(ed.get("school"))
        if any(s in school for s in TOP_SCHOOL_ALIASES):
            bg_school = True

    blob_exp = to_text(" ".join(blob_exp_parts))
    full_blob = to_text(blob_head, blob_exp)

    score = 0

    if any(t in blob_head for t in STEALTH_TERMS):
        score += 20
    if founder_hits > 0:
        score += 10

    if current_recent > 0:
        score += 12
    if current_recent == 0 and any(t in blob_head for t in ["building", "stealth"]):
        score += 6
    if ended_recent > 0:
        score += 8

    if bg_company:
        score += 9
    if bg_school:
        score += 6

    ind = 0
    if industry_ai:
        ind += 7
    if industry_fin:
        ind += 5
    if industry_health:
        ind += 3
    score += min(15, ind)

    if any(g in full_blob for g in GEO_TERMS):
        score += 10

    if any(a in full_blob for a in ACCEL_TERMS):
        score += 10

    if email:
        score += 6
    if any(t in blob_head for t in OUTREACH_TERMS):
        score += 4

    penalties = 0
    if bigco_exec_flag and not any(t in blob_head for t in STEALTH_TERMS):
        penalties += 10
    if (follower_count or 0) > 50000 and not any(t in blob_head for t in STEALTH_TERMS):
        penalties += 5
    if founder_hits == 0 and current_recent == 0 and not any(t in blob_head for t in STEALTH_TERMS):
        penalties += 5

    score = max(0, min(100, score - penalties))

    if score >= 75:
        tier = "A"
    elif score >= 60:
        tier = "B"
    else:
        tier = "C"

    return {
        "name": (basic.get("fullname") or "").strip(),
        "url": profile_url,
        "headline": (headline or "").strip(),
        "location": (location.get("full") or location.get("city") or location.get("country") or "").strip(),
        "score": score,
        "tier": tier,
        "email": email,
    }


def main():
    data_a = []
    data_b = []
    if os.path.exists(INPUT_PREF):
        with open(INPUT_PREF, "r") as f:
            try:
                data_a = json.load(f)
            except Exception:
                data_a = []
    if os.path.exists(INPUT_FALLBACK):
        with open(INPUT_FALLBACK, "r") as f:
            try:
                data_b = json.load(f)
            except Exception:
                data_b = []

    if not data_a and not data_b:
        print(f"❌ Missing inputs. Expected at least one of {INPUT_PREF} or {INPUT_FALLBACK}.")
        return

    combined = dedupe_profiles(data_a if isinstance(data_a, list) else [], data_b if isinstance(data_b, list) else [])
    print(f"📥 Loaded {len(combined)} unique profiles (combined)")

    scored = [score_profile(p) for p in combined]

    with open(OUT_JSON, "w") as f:
        json.dump(scored, f, indent=2)

    def write_csv(filepath: str, rows: List[Dict[str, Any]]):
        with open(filepath, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "url", "headline", "location", "score", "tier", "email"])
            for r in rows:
                w.writerow([r.get("name", ""), r.get("url", ""), r.get("headline", ""), r.get("location", ""), r.get("score", 0), r.get("tier", ""), r.get("email") or ""])

    write_csv(OUT_CSV, scored)

    summary = {"A": 0, "B": 0, "C": 0}
    for r in scored:
        t = r.get("tier")
        if t in summary:
            summary[t] += 1
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)

    write_csv(OUT_A, [r for r in scored if r.get("tier") == "A"])
    write_csv(OUT_B, [r for r in scored if r.get("tier") == "B"])

    print(f"✅ Scored {len(scored)} profiles")
    print(f"🏷️ Tiers: A={summary['A']} | B={summary['B']} | C={summary['C']}")
    print(f"📄 Outputs: {OUT_JSON}, {OUT_CSV}, {OUT_SUMMARY}, {OUT_A}, {OUT_B}")


if __name__ == "__main__":
    main()
