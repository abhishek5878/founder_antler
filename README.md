# 🚀 Antler Stealth Founder Sourcing (Easy Guide)

Find real LinkedIn founders in/near stealth, enrich their profiles, and score them into Tier A/B/C for outreach.

## ✅ What you get
- 100+ real profiles (current total: 369)
- Full profile sections (experience, education, location, email if public)
- Scored tiers ready for outreach

Key files
- `apimaestro_scored_tierA.csv` — top targets
- `apimaestro_scored_tierB.csv` — next best
- `apimaestro_scored.csv` — all scored
- `apimaestro_scored_summary.json` — counts

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
- Stealth & founder (30): headline/about has “stealth/building/working on/exploring”; current title has founder/cofounder
- Recency (20): current role started in 2023/24; recent transition
- Background (15): top companies (Google/Meta/Amazon/Microsoft/Apple/Stripe/Airbnb/Tesla/OpenAI) and schools (Stanford/Harvard/MIT/Berkeley/Oxford/Cambridge/Wharton/IIT/IIM)
- Industry (≤15): AI (+7), Fintech (+5), Health (+3)
- Geography (10): SF/NYC/London/Singapore/Bangalore/Berlin/Stockholm/Paris/Sydney
- Network (10): YC/Techstars/500/Antler/cohort/batch
- Outreach (10): email present; “hiring/open to/seeking/building”

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
- “Hi [Name], noticed you’re [building/stealth] in [AI/fintech/health]. Background at [Company/School] stood out. Open to a 15‑min chat on [problem]?”

## 🔎 Notes
- Public data only via Apify actors; batching avoids rate limits
- All API usage via env vars; no secrets in repo
