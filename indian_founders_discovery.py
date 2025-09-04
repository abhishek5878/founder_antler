#!/usr/bin/env python3
"""
Indian Founders Discovery - Health, Health x AI, Consumer Tech, Consumer x AI
Targets Indian founders building in specific verticals for Antler
"""

import os
import json
import time
from typing import List, Dict, Any
import requests
from serpapi import GoogleSearch

# API Keys
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

# Indian cities and regions
INDIAN_LOCATIONS = [
    "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", 
    "Gurgaon", "Noida", "Ahmedabad", "Kolkata", "Jaipur", "Indore",
    "Chandigarh", "Vadodara", "Surat", "Nagpur", "Lucknow", "Kanpur",
    "Patna", "Bhopal", "Ludhiana", "Agra", "Varanasi", "Srinagar",
    "Amritsar", "Allahabad", "Ranchi", "Howrah", "Coimbatore", "Vishakhapatnam"
]

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
    "AI", "artificial intelligence", "machine learning", "ML", "deep learning",
    "computer vision", "NLP", "natural language processing", "predictive analytics",
    "data science", "algorithm", "automation", "intelligent", "smart"
]

def generate_search_queries() -> List[str]:
    """Generate targeted search queries for Indian founders in health/consumer tech"""
    queries = []
    
    # Base patterns for Indian founders
    base_patterns = [
        'site:linkedin.com/in/ "founder" AND ("India" OR "Indian" OR "Bangalore" OR "Mumbai" OR "Delhi" OR "Hyderabad")',
        'site:linkedin.com/in/ "building" AND ("India" OR "Indian" OR "Bangalore" OR "Mumbai" OR "Delhi" OR "Hyderabad")',
        'site:linkedin.com/in/ "stealth" AND ("India" OR "Indian" OR "Bangalore" OR "Mumbai" OR "Delhi" OR "Hyderabad")',
        'site:linkedin.com/in/ "startup" AND ("India" OR "Indian" OR "Bangalore" OR "Mumbai" OR "Delhi" OR "Hyderabad")',
        'site:linkedin.com/in/ "co-founder" AND ("India" OR "Indian" OR "Bangalore" OR "Mumbai" OR "Delhi" OR "Hyderabad")',
        'site:linkedin.com/in/ "CEO" AND ("India" OR "Indian" OR "Bangalore" OR "Mumbai" OR "Delhi" OR "Hyderabad") AND ("2023" OR "2024")',
    ]
    
    # Health-specific queries
    for health_keyword in HEALTH_KEYWORDS[:15]:  # Top 15 health keywords
        for location in INDIAN_LOCATIONS[:10]:   # Top 10 locations
            queries.append(f'site:linkedin.com/in/ "{health_keyword}" AND "{location}" AND ("founder" OR "building" OR "startup")')
            queries.append(f'site:linkedin.com/in/ "{health_keyword}" AND "India" AND ("founder" OR "building" OR "startup")')
    
    # Consumer tech queries
    for consumer_keyword in CONSUMER_TECH_KEYWORDS[:15]:  # Top 15 consumer keywords
        for location in INDIAN_LOCATIONS[:10]:   # Top 10 locations
            queries.append(f'site:linkedin.com/in/ "{consumer_keyword}" AND "{location}" AND ("founder" OR "building" OR "startup")')
            queries.append(f'site:linkedin.com/in/ "{consumer_keyword}" AND "India" AND ("founder" OR "building" OR "startup")')
    
    # Health x AI queries
    for health_keyword in HEALTH_KEYWORDS[:10]:
        for ai_keyword in AI_KEYWORDS[:8]:
            queries.append(f'site:linkedin.com/in/ "{health_keyword}" AND "{ai_keyword}" AND "India" AND ("founder" OR "building" OR "startup")')
    
    # Consumer x AI queries
    for consumer_keyword in CONSUMER_TECH_KEYWORDS[:10]:
        for ai_keyword in AI_KEYWORDS[:8]:
            queries.append(f'site:linkedin.com/in/ "{consumer_keyword}" AND "{ai_keyword}" AND "India" AND ("founder" OR "building" OR "startup")')
    
    # Recent graduates and transitions
    recent_patterns = [
        'site:linkedin.com/in/ ("IIT" OR "IIM" OR "BITS" OR "NIT") AND ("2023" OR "2024") AND ("founder" OR "building" OR "startup")',
        'site:linkedin.com/in/ ("ex-Google" OR "ex-Microsoft" OR "ex-Amazon" OR "ex-Meta") AND "India" AND ("founder" OR "building" OR "startup")',
        'site:linkedin.com/in/ ("ex-Flipkart" OR "ex-Paytm" OR "ex-Ola" OR "ex-Swiggy" OR "ex-Zomato") AND ("founder" OR "building" OR "startup")',
    ]
    
    queries.extend(base_patterns)
    queries.extend(recent_patterns)
    
    return list(set(queries))  # Remove duplicates

def search_serpapi(query: str, num_pages: int = 2) -> List[str]:
    """Search Google via SerpAPI and extract LinkedIn URLs"""
    linkedin_urls = []
    
    try:
        for page in range(num_pages):
            search = GoogleSearch({
                "q": query,
                "api_key": SERPAPI_KEY,
                "start": page * 10,
                "num": 10
            })
            
            results = search.get_dict()
            
            if "organic_results" in results:
                for result in results["organic_results"]:
                    url = result.get("link", "")
                    if "linkedin.com/in/" in url:
                        # Clean the URL
                        if "?" in url:
                            url = url.split("?")[0]
                        linkedin_urls.append(url)
            
            time.sleep(1)  # Rate limiting
            
    except Exception as e:
        print(f"Error searching for query '{query}': {e}")
    
    return linkedin_urls

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
            
            print(f"Processed batch {i//batch_size + 1}: {len(batch)} profiles")
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
    
    return all_results

def filter_indian_health_consumer_profiles(profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter profiles for Indian founders in health/consumer tech"""
    filtered_profiles = []
    
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
        
        # Filter criteria: Indian + (Health OR Consumer) + (AI OR no AI) + Founder
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
            
            filtered_profiles.append(profile)
    
    return filtered_profiles

def main():
    """Main execution function"""
    print("🚀 Indian Founders Discovery - Health & Consumer Tech")
    print("=" * 60)
    
    # Step 1: Generate search queries
    print("\n1️⃣ Generating targeted search queries...")
    queries = generate_search_queries()
    print(f"Generated {len(queries)} search queries")
    
    # Step 2: Search for LinkedIn URLs
    print("\n2️⃣ Searching for LinkedIn profiles...")
    all_urls = []
    
    for i, query in enumerate(queries[:30]):  # Limit to top 30 queries for speed
        print(f"Searching query {i+1}/{min(30, len(queries))}: {query[:80]}...")
        urls = search_serpapi(query, num_pages=1)
        all_urls.extend(urls)
        time.sleep(1)  # Rate limiting
    
    # Remove duplicates
    unique_urls = list(set(all_urls))
    print(f"\nFound {len(unique_urls)} unique LinkedIn URLs")
    
    # Save URLs
    with open("indian_founders_urls.json", "w") as f:
        json.dump(unique_urls, f, indent=2)
    
    # Step 3: Enrich profiles via Apify
    print("\n3️⃣ Enriching profiles via Apify...")
    enriched_profiles = run_apify_batch_scrape(unique_urls)
    print(f"Enriched {len(enriched_profiles)} profiles")
    
    # Save raw enriched data
    with open("indian_founders_raw.json", "w") as f:
        json.dump(enriched_profiles, f, indent=2)
    
    # Step 4: Filter for Indian health/consumer founders
    print("\n4️⃣ Filtering for Indian health/consumer founders...")
    filtered_profiles = filter_indian_health_consumer_profiles(enriched_profiles)
    print(f"Filtered to {len(filtered_profiles)} Indian health/consumer founders")
    
    # Save filtered data
    with open("indian_founders_filtered.json", "w") as f:
        json.dump(filtered_profiles, f, indent=2)
    
    # Step 5: Generate summary
    print("\n5️⃣ Generating summary...")
    summary = {
        "total_urls_found": len(unique_urls),
        "total_profiles_enriched": len(enriched_profiles),
        "indian_health_consumer_founders": len(filtered_profiles),
        "categories": {},
        "locations": {},
        "ai_adoption": {"with_ai": 0, "without_ai": 0}
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
    
    # Save summary
    with open("indian_founders_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n✅ Discovery Complete!")
    print(f"📊 Found {len(filtered_profiles)} Indian founders in health/consumer tech")
    print(f"🏥 Categories: {summary['categories']}")
    print(f"📍 Top locations: {dict(list(summary['locations'].items())[:5])}")
    print(f"🤖 AI adoption: {summary['ai_adoption']}")
    
    print("\n📁 Output files:")
    print("- indian_founders_urls.json: Discovered LinkedIn URLs")
    print("- indian_founders_raw.json: Raw enriched profiles")
    print("- indian_founders_filtered.json: Filtered Indian health/consumer founders")
    print("- indian_founders_summary.json: Summary statistics")

if __name__ == "__main__":
    main()
