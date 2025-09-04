#!/usr/bin/env python3
"""
Indian Founders from Existing URLs - Health & Consumer Tech Focus
Filters existing LinkedIn URLs for Indian founders and enriches them
"""

import json
import os
import time
import requests
from typing import List, Dict, Any

# API Keys
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

def filter_indian_urls() -> List[str]:
    """Filter existing URLs for Indian profiles"""
    try:
        with open("serpapi_linkedin_urls.json", "r") as f:
            all_urls = json.load(f)
    except FileNotFoundError:
        print("❌ serpapi_linkedin_urls.json not found")
        return []
    
    indian_urls = []
    for url in all_urls:
        if "in.linkedin.com" in url or "linkedin.com/in/" in url:
            # Additional check for Indian names/patterns in URL
            username = url.split("linkedin.com/in/")[-1].split("/")[0].split("?")[0]
            if username and len(username) > 2:
                indian_urls.append(url)
    
    print(f"📊 Found {len(indian_urls)} Indian LinkedIn URLs from {len(all_urls)} total URLs")
    return indian_urls

def run_apify_batch_scrape(profile_urls: List[str]) -> List[Dict[str, Any]]:
    """Run Apify batch scraper to get detailed profile data"""
    if not profile_urls:
        return []
    
    # Extract usernames from URLs
    usernames = []
    for url in profile_urls:
        if "linkedin.com/in/" in url:
            username = url.split("linkedin.com/in/")[-1].split("/")[0].split("?")[0]
            if username and len(username) > 2:
                usernames.append(username)
    
    if not usernames:
        return []
    
    print(f"🔍 Enriching {len(usernames)} Indian profiles via Apify...")
    
    # Split into batches of 50 (Apify limit)
    batch_size = 50
    all_results = []
    
    for i in range(0, len(usernames), batch_size):
        batch = usernames[i:i + batch_size]
        
        try:
            url = "https://api.apify.com/v2/acts/apimaestro~linkedin-profile-batch-scraper-no-cookies-required/run-sync-get-dataset-items"
            
            params = {
                "token": APIFY_TOKEN,
                "usernames": batch
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            results = response.json()
            if isinstance(results, list):
                all_results.extend(results)
            
            print(f"✅ Processed batch {i//batch_size + 1}: {len(batch)} profiles")
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error processing batch {i//batch_size + 1}: {e}")
    
    return all_results

def filter_health_consumer_profiles(profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter profiles for health and consumer tech focus"""
    filtered_profiles = []
    
    # Health and Consumer Tech Keywords
    HEALTH_KEYWORDS = [
        "healthtech", "health tech", "healthcare", "health care", "medical", "pharma",
        "telemedicine", "tele-medicine", "digital health", "mental health", "fitness",
        "wellness", "nutrition", "diagnostics", "biotech", "biotechnology", "clinical",
        "patient care", "hospital", "clinic", "doctor", "physician", "nurse",
        "medical device", "health insurance", "healthcare platform", "health app"
    ]
    
    CONSUMER_TECH_KEYWORDS = [
        "consumer tech", "consumer technology", "e-commerce", "ecommerce", "marketplace",
        "retail tech", "retail technology", "fashion tech", "food tech", "foodtech",
        "fintech", "financial technology", "payments", "banking", "lending",
        "insurance tech", "insurtech", "real estate", "proptech", "property tech",
        "travel tech", "traveltech", "education tech", "edtech", "learning",
        "entertainment", "gaming", "media", "content", "social", "mobile app",
        "consumer app", "B2C", "direct to consumer", "D2C", "subscription"
    ]
    
    AI_KEYWORDS = [
        "ai", "artificial intelligence", "machine learning", "ml", "deep learning",
        "computer vision", "nlp", "natural language processing", "predictive analytics",
        "data science", "algorithm", "automation", "intelligent", "smart"
    ]
    
    for profile in profiles:
        if not profile:
            continue
            
        # Extract text content for analysis
        headline = profile.get("headline", "").lower()
        about = profile.get("about", "").lower()
        location = profile.get("location", "").lower()
        
        # Check for Indian indicators
        indian_indicators = [
            "india", "indian", "bangalore", "mumbai", "delhi", "hyderabad", 
            "chennai", "pune", "gurgaon", "noida", "ahmedabad", "kolkata",
            "iit", "iim", "bits", "nit", "indian institute"
        ]
        
        is_indian = any(indicator in location or indicator in about for indicator in indian_indicators)
        
        # Check for health/consumer tech indicators
        health_indicators = [kw.lower() for kw in HEALTH_KEYWORDS]
        consumer_indicators = [kw.lower() for kw in CONSUMER_TECH_KEYWORDS]
        ai_indicators = [kw.lower() for kw in AI_KEYWORDS]
        
        has_health = any(indicator in headline or indicator in about for indicator in health_indicators)
        has_consumer = any(indicator in headline or indicator in about for indicator in consumer_indicators)
        has_ai = any(indicator in headline or indicator in about for indicator in ai_indicators)
        
        # Check for founder/startup indicators
        founder_indicators = [
            "founder", "co-founder", "cofounder", "ceo", "startup", "building", 
            "stealth", "working on", "exploring", "launching"
        ]
        
        is_founder = any(indicator in headline or indicator in about for indicator in founder_indicators)
        
        # Filter criteria: Indian + (Health OR Consumer) + Founder
        if is_indian and (has_health or has_consumer) and is_founder:
            # Add category tags
            categories = []
            if has_health and has_ai:
                categories.append("Health x AI")
            elif has_health:
                categories.append("Health")
            elif has_consumer and has_ai:
                categories.append("Consumer x AI")
            elif has_consumer:
                categories.append("Consumer Tech")
            
            profile["categories"] = categories
            profile["is_indian"] = True
            profile["has_ai"] = has_ai
            profile["has_health"] = has_health
            profile["has_consumer"] = has_consumer
            
            filtered_profiles.append(profile)
    
    return filtered_profiles

def main():
    """Main execution function"""
    print("🇮🇳 Indian Founders from Existing URLs - Health & Consumer Tech")
    print("=" * 70)
    
    # Step 1: Filter Indian URLs from existing data
    print("\n1️⃣ Filtering Indian URLs from existing data...")
    indian_urls = filter_indian_urls()
    
    if not indian_urls:
        print("❌ No Indian URLs found. Exiting.")
        return
    
    # Save Indian URLs
    with open("indian_founders_urls_filtered.json", "w") as f:
        json.dump(indian_urls, f, indent=2)
    
    # Step 2: Enrich profiles via Apify
    print("\n2️⃣ Enriching profiles via Apify...")
    enriched_profiles = run_apify_batch_scrape(indian_urls)
    print(f"✅ Enriched {len(enriched_profiles)} profiles")
    
    # Save raw enriched data
    with open("indian_founders_raw_enriched.json", "w") as f:
        json.dump(enriched_profiles, f, indent=2)
    
    # Step 3: Filter for health/consumer tech focus
    print("\n3️⃣ Filtering for health/consumer tech focus...")
    filtered_profiles = filter_health_consumer_profiles(enriched_profiles)
    print(f"✅ Filtered to {len(filtered_profiles)} Indian health/consumer founders")
    
    # Save filtered data
    with open("indian_founders_filtered_final.json", "w") as f:
        json.dump(filtered_profiles, f, indent=2)
    
    # Step 4: Generate summary
    print("\n4️⃣ Generating summary...")
    summary = {
        "total_indian_urls": len(indian_urls),
        "total_profiles_enriched": len(enriched_profiles),
        "indian_health_consumer_founders": len(filtered_profiles),
        "categories": {},
        "locations": {},
        "ai_adoption": {"with_ai": 0, "without_ai": 0},
        "focus_areas": {"health": 0, "consumer": 0, "both": 0}
    }
    
    for profile in filtered_profiles:
        # Count categories
        for category in profile.get("categories", []):
            summary["categories"][category] = summary["categories"].get(category, 0) + 1
        
        # Count locations
        location = profile.get("location", "Unknown")
        summary["locations"][location] = summary["locations"].get(location, 0) + 1
        
        # Count AI adoption
        if profile.get("has_ai"):
            summary["ai_adoption"]["with_ai"] += 1
        else:
            summary["ai_adoption"]["without_ai"] += 1
        
        # Count focus areas
        has_health = profile.get("has_health", False)
        has_consumer = profile.get("has_consumer", False)
        
        if has_health and has_consumer:
            summary["focus_areas"]["both"] += 1
        elif has_health:
            summary["focus_areas"]["health"] += 1
        elif has_consumer:
            summary["focus_areas"]["consumer"] += 1
    
    # Save summary
    with open("indian_founders_summary_final.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n✅ Discovery Complete!")
    print(f"📊 Found {len(filtered_profiles)} Indian founders in health/consumer tech")
    print(f"🏥 Categories: {summary['categories']}")
    print(f"📍 Top locations: {dict(list(summary['locations'].items())[:5])}")
    print(f"🤖 AI adoption: {summary['ai_adoption']}")
    print(f"🎯 Focus areas: {summary['focus_areas']}")
    
    print("\n📁 Output files:")
    print("- indian_founders_urls_filtered.json: Filtered Indian LinkedIn URLs")
    print("- indian_founders_raw_enriched.json: Raw enriched profiles")
    print("- indian_founders_filtered_final.json: Final filtered Indian health/consumer founders")
    print("- indian_founders_summary_final.json: Summary statistics")
    
    # Step 5: Run scoring if we have profiles
    if filtered_profiles:
        print("\n5️⃣ Running scoring system...")
        try:
            # Save filtered profiles in the format expected by scoring script
            with open("indian_founders_filtered.json", "w") as f:
                json.dump(filtered_profiles, f, indent=2)
            
            # Run scoring
            import subprocess
            result = subprocess.run(["python3", "score_indian_founders.py"], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
                
        except Exception as e:
            print(f"❌ Error running scoring: {e}")

if __name__ == "__main__":
    main()
