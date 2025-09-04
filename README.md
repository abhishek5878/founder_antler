# 🚀 Indian Early-Stage Founders - Health & Consumer Tech

Find real early-stage Indian founders building in stealth or just starting out in health, health x AI, consumer tech, and consumer x AI.

## ✅ What you get
- 20+ real early-stage Indian founders (not established ones)
- Focus on stealth mode and early-stage startups
- Health, Health x AI, Consumer Tech, Consumer x AI categories
- Scored tiers ready for outreach

Key files
- `indian_early_stage_tierA.csv` — top targets (19 founders)
- `indian_early_stage_tierB.csv` — next best (1 founder)
- `indian_early_stage_founders.csv` — all founders
- `indian_early_stage_summary.json` — counts

## 🎯 Target Profile Types
- **Recent Graduates (2023-2024)**: IIT/IIM/BITS graduates building startups
- **Ex-FAANG Engineers**: Google, Meta, Amazon, Microsoft, Apple alumni
- **Ex-Indian Unicorn Employees**: Flipkart, Paytm, Razorpay, BYJU'S alumni
- **Stealth Mode Founders**: Building in stealth with strong backgrounds
- **Early Stage Startups**: Just starting out, pre-seed/seed stage

## 🔐 Environment (no keys in code)
Set these once in your terminal before running:
```
export SERPAPI_KEY=your_serpapi_key
export APIFY_TOKEN=your_apify_token
```

## 🏃 Quick start (two steps)
1) Enrich profiles (from discovered URLs)
```
python3 apify_batch_scrape.py
```
- Output: `apimaestro_batch_raw.json`
- Optional richer: `python3 apify_apimaestro_pipeline.py` → `apimaestro_full_sections_raw.json`

2) Score and export tiers (combines & de‑dupes automatically)
```
python3 score_apimaestro.py
```
- Outputs: `apimaestro_scored_tierA.csv`, `apimaestro_scored_tierB.csv`, `apimaestro_scored.csv`, `apimaestro_scored_summary.json`

## 🧩 What Tier A/B/C means
- **Tier A (75–100)**: clear stealth intent + recent (2023/24) founder signal + strong fit
- **Tier B (60–74)**: promising; fewer signals or less recent
- **Tier C (<60)**: weak/no stealth signals

## 📏 Scoring (0–100, explainable)
Adds points for:
- Stealth & founder (30): headline/about has "stealth/building/working on/exploring"; current title has founder/cofounder
- Recency (20): current role started in 2023/24; recent transition
- Background (15): top companies (Google/Meta/Amazon/Microsoft/Apple/Stripe/Airbnb/Tesla/OpenAI) and schools (Stanford/Harvard/MIT/Berkeley/Oxford/Cambridge/Wharton/IIT/IIM)
- Industry (≤15): AI (+7), Fintech (+5), Health (+3)
- Geography (10): SF/NYC/London/Singapore/Bangalore/Berlin/Stockholm/Paris/Sydney
- Network (10): YC/Techstars/500/Antler/cohort/batch
- Outreach (10): email present; "hiring/open to/seeking/building"

Penalties (≤20): big‑company exec with no stealth; huge audience with no stealth; no founder/recency/stealth.

## 📦 Full pipeline (optional)
- Discover + Enrich via SerpAPI→Apify
```
python3 serpapi_to_apify.py
```
- Batch enrichment only (fast)
```
python3 apify_batch_scrape.py
```
- Full sections + optional email
```
python3 apify_apimaestro_pipeline.py
```
- Score & export tiers
```
python3 score_apimaestro.py
```

## 📁 Useful files
- Data: `serpapi_linkedin_urls.json`, `apimaestro_batch_raw.json`, `apimaestro_full_sections_stealth.json`
- Outputs: `apimaestro_scored_tierA.csv`, `apimaestro_scored_tierB.csv`, `apimaestro_scored.csv`, `apimaestro_scored_summary.json`

## ✉️ Outreach (Tier A/B)
- "Hi [Name], noticed you're [building/stealth] in [AI/fintech/health]. Background at [Company/School] stood out. Open to a 15‑min chat on [problem]?"

## 🔎 Notes
- Public data only via Apify actors; batching avoids rate limits
- All API usage via env vars; no secrets in repo

## 🇮🇳 Indian Early-Stage Founders Summary
- **Total**: 20 real early-stage founders
- **Tier A**: 19 founders (95%)
- **Tier B**: 1 founder (5%)
- **AI Adoption**: 19 with AI (95%), 1 without AI (5%)
- **Stages**: 11 stealth mode, 9 early stage
- **Backgrounds**: 10 ex-FAANG, 5 ex-unicorns, 1 recent graduate, 4 others
- **Categories**: 6 Health x AI, 13 Consumer x AI, 1 Health
- **Top Locations**: Bangalore (4), Mumbai (3), Delhi (3), Hyderabad (2), Gurgaon (1)
