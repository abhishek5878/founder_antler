#!/usr/bin/env python3
"""
Filter Existing Data for Indian Founders - Health & Consumer Tech
Filters existing apimaestro_batch_raw.json for Indian founders in specific verticals
"""

import json
from typing import List, Dict, Any

def filter_indian_health_consumer_profiles() -> List[Dict[str, Any]]:
    """Filter existing profiles for Indian founders in health/consumer tech"""
    
    # Load existing data
    try:
        with open("apimaestro_batch_raw.json", "r") as f:
            all_profiles = json.load(f)
    except FileNotFoundError:
        print("❌ apimaestro_batch_raw.json not found")
        return []
    
    print(f"📊 Processing {len(all_profiles)} existing profiles...")
    
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
    
    filtered_profiles = []
    indian_count = 0
    
    for profile in all_profiles:
        if not profile:
            continue
            
        # Extract text content for analysis
        headline = profile.get("headline", "").lower()
        about = profile.get("about", "").lower()
        location = profile.get("location", "").lower()
        experience = profile.get("experience", [])
        education = profile.get("education", [])
        
        # Check for Indian indicators
        indian_indicators = [
            "india", "indian", "bangalore", "mumbai", "delhi", "hyderabad", 
            "chennai", "pune", "gurgaon", "noida", "ahmedabad", "kolkata",
            "iit", "iim", "bits", "nit", "indian institute"
        ]
        
        is_indian = any(indicator in location or indicator in about for indicator in indian_indicators)
        
        if is_indian:
            indian_count += 1
            
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
            if (has_health or has_consumer) and is_founder:
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
    
    print(f"🇮🇳 Found {indian_count} Indian profiles out of {len(all_profiles)} total")
    print(f"🎯 Filtered to {len(filtered_profiles)} Indian health/consumer founders")
    
    return filtered_profiles

def generate_summary(filtered_profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics"""
    summary = {
        "total_profiles": len(filtered_profiles),
        "categories": {},
        "locations": {},
        "ai_adoption": {"with_ai": 0, "without_ai": 0},
        "focus_areas": {"health": 0, "consumer": 0, "both": 0},
        "top_companies": {},
        "top_schools": {}
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
        
        # Count top companies
        experience = profile.get("experience", [])
        for exp in experience:
            company = exp.get("company", "")
            if company:
                summary["top_companies"][company] = summary["top_companies"].get(company, 0) + 1
        
        # Count top schools
        education = profile.get("education", [])
        for edu in education:
            school = edu.get("school", "")
            if school:
                summary["top_schools"][school] = summary["top_schools"].get(school, 0) + 1
    
    return summary

def main():
    """Main execution function"""
    print("🇮🇳 Filtering Existing Data for Indian Founders - Health & Consumer Tech")
    print("=" * 75)
    
    # Filter profiles
    filtered_profiles = filter_indian_health_consumer_profiles()
    
    if not filtered_profiles:
        print("❌ No Indian health/consumer founders found. Exiting.")
        return
    
    # Generate summary
    summary = generate_summary(filtered_profiles)
    
    # Save filtered data
    with open("indian_founders_filtered.json", "w") as f:
        json.dump(filtered_profiles, f, indent=2)
    
    # Save summary
    with open("indian_founders_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n✅ Filtering Complete!")
    print(f"📊 Found {len(filtered_profiles)} Indian founders in health/consumer tech")
    print(f"🏥 Categories: {summary['categories']}")
    print(f"📍 Top locations: {dict(list(summary['locations'].items())[:5])}")
    print(f"🤖 AI adoption: {summary['ai_adoption']}")
    print(f"🎯 Focus areas: {summary['focus_areas']}")
    
    # Show top companies and schools
    top_companies = sorted(summary["top_companies"].items(), key=lambda x: x[1], reverse=True)[:10]
    top_schools = sorted(summary["top_schools"].items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"🏢 Top companies: {dict(top_companies)}")
    print(f"🎓 Top schools: {dict(top_schools)}")
    
    print("\n📁 Output files:")
    print("- indian_founders_filtered.json: Filtered Indian health/consumer founders")
    print("- indian_founders_summary.json: Summary statistics")
    
    # Run scoring if we have profiles
    if filtered_profiles:
        print("\n🎯 Running scoring system...")
        try:
            import subprocess
            result = subprocess.run(["python3", "score_indian_founders.py"], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
                
        except Exception as e:
            print(f"❌ Error running scoring: {e}")

if __name__ == "__main__":
    main()
