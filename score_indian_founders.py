#!/usr/bin/env python3
"""
Indian Founders Scoring - Health, Health x AI, Consumer Tech, Consumer x AI
Custom scoring system optimized for Indian founders in specific verticals
"""

import json
import re
from typing import Dict, Any, List
from datetime import datetime

def extract_signals(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant signals from profile data"""
    signals = {
        "stealth_founder": False,
        "recency": False,
        "indian_background": False,
        "health_focus": False,
        "consumer_focus": False,
        "ai_focus": False,
        "top_companies": [],
        "top_schools": [],
        "geography": "",
        "network": [],
        "outreach_ready": False,
        "penalties": []
    }
    
    # Extract text content
    headline = profile_data.get("headline", "").lower()
    about = profile_data.get("about", "").lower()
    location = profile_data.get("location", "").lower()
    experience = profile_data.get("experience", [])
    education = profile_data.get("education", [])
    
    # Stealth & Founder signals
    stealth_keywords = ["stealth", "building", "working on", "exploring", "launching", "founding"]
    founder_keywords = ["founder", "co-founder", "cofounder", "ceo", "startup"]
    
    signals["stealth_founder"] = (
        any(keyword in headline or keyword in about for keyword in stealth_keywords) and
        any(keyword in headline or keyword in about for keyword in founder_keywords)
    )
    
    # Recency signals (2023/24 activity)
    current_year = datetime.now().year
    recency_indicators = [
        str(current_year), str(current_year - 1),
        "recent", "new", "just", "recently", "latest"
    ]
    signals["recency"] = any(indicator in headline or indicator in about for indicator in recency_indicators)
    
    # Indian background signals
    indian_indicators = [
        "india", "indian", "bangalore", "mumbai", "delhi", "hyderabad", 
        "chennai", "pune", "gurgaon", "noida", "ahmedabad", "kolkata",
        "iit", "iim", "bits", "nit", "indian institute"
    ]
    signals["indian_background"] = any(indicator in location or indicator in about for indicator in indian_indicators)
    
    # Health focus signals
    health_keywords = [
        "healthtech", "health tech", "healthcare", "health care", "medical", "pharma",
        "telemedicine", "digital health", "mental health", "fitness", "wellness",
        "nutrition", "diagnostics", "biotech", "clinical", "patient care",
        "hospital", "clinic", "doctor", "physician", "nurse", "medical device"
    ]
    signals["health_focus"] = any(keyword in headline or keyword in about for keyword in health_keywords)
    
    # Consumer tech focus signals
    consumer_keywords = [
        "consumer tech", "consumer technology", "e-commerce", "ecommerce", "marketplace",
        "retail tech", "fashion tech", "food tech", "foodtech", "fintech", "payments",
        "insurtech", "proptech", "travel tech", "edtech", "entertainment", "gaming",
        "mobile app", "consumer app", "B2C", "D2C", "subscription"
    ]
    signals["consumer_focus"] = any(keyword in headline or keyword in about for keyword in consumer_keywords)
    
    # AI focus signals
    ai_keywords = [
        "ai", "artificial intelligence", "machine learning", "ml", "deep learning",
        "computer vision", "nlp", "natural language processing", "predictive analytics",
        "data science", "algorithm", "automation", "intelligent", "smart"
    ]
    signals["ai_focus"] = any(keyword in headline or keyword in about for keyword in ai_keywords)
    
    # Top companies (Indian and global)
    top_companies = [
        "google", "microsoft", "amazon", "meta", "apple", "stripe", "airbnb", "tesla", "openai",
        "flipkart", "paytm", "ola", "swiggy", "zomato", "razorpay", "phonepe", "byju's",
        "cred", "dunzo", "meesho", "upgrad", "unacademy", "whitehat jr", "cure.fit",
        "practo", "1mg", "pharmeasy", "netmeds", "healthkart", "cult.fit"
    ]
    
    for exp in experience:
        company = exp.get("company", "").lower()
        if any(top_company in company for top_company in top_companies):
            signals["top_companies"].append(exp.get("company", ""))
    
    # Top schools (Indian and global)
    top_schools = [
        "stanford", "harvard", "mit", "berkeley", "oxford", "cambridge", "wharton",
        "iit", "iim", "bits", "nit", "delhi university", "bombay university",
        "calcutta university", "madras university", "anna university", "vit",
        "manipal", "amrita", "srm", "thapar", "birla institute"
    ]
    
    for edu in education:
        school = edu.get("school", "").lower()
        if any(top_school in school for top_school in top_schools):
            signals["top_schools"].append(edu.get("school", ""))
    
    # Geography
    indian_cities = [
        "bangalore", "mumbai", "delhi", "hyderabad", "chennai", "pune", 
        "gurgaon", "noida", "ahmedabad", "kolkata", "jaipur", "indore"
    ]
    
    for city in indian_cities:
        if city in location:
            signals["geography"] = city.title()
            break
    
    # Network/Accelerator signals
    network_keywords = [
        "yc", "y combinator", "techstars", "500 startups", "antler", "cohort", "batch",
        "startup india", "nasscom", "tiie", "iit incubator", "iim incubator"
    ]
    
    for keyword in network_keywords:
        if keyword in headline or keyword in about:
            signals["network"].append(keyword)
    
    # Outreach readiness
    outreach_indicators = [
        "hiring", "open to", "seeking", "looking for", "building team", "growing",
        "email", "contact", "reach out", "connect", "collaborate"
    ]
    signals["outreach_ready"] = any(indicator in headline or indicator in about for indicator in outreach_indicators)
    
    # Penalties
    penalty_indicators = [
        "established", "senior", "veteran", "20+ years", "15+ years", "10+ years",
        "executive", "director", "vp", "head of", "chief", "president",
        "massive audience", "influencer", "thought leader", "speaker"
    ]
    
    for indicator in penalty_indicators:
        if indicator in headline or indicator in about:
            signals["penalties"].append(indicator)
    
    return signals

def calculate_score(signals: Dict[str, Any], profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate score based on extracted signals"""
    score = 0
    breakdown = {}
    
    # Stealth & Founder (30 points)
    if signals["stealth_founder"]:
        score += 30
        breakdown["stealth_founder"] = 30
    else:
        breakdown["stealth_founder"] = 0
    
    # Recency (20 points)
    if signals["recency"]:
        score += 20
        breakdown["recency"] = 20
    else:
        breakdown["recency"] = 0
    
    # Indian Background (15 points)
    if signals["indian_background"]:
        score += 15
        breakdown["indian_background"] = 15
    else:
        breakdown["indian_background"] = 0
    
    # Health/Consumer Focus (15 points)
    focus_score = 0
    if signals["health_focus"]:
        focus_score += 8
    if signals["consumer_focus"]:
        focus_score += 8
    if signals["ai_focus"]:
        focus_score += 4
    
    score += min(focus_score, 15)
    breakdown["health_consumer_focus"] = min(focus_score, 15)
    
    # Top Companies (10 points)
    company_score = min(len(signals["top_companies"]) * 2, 10)
    score += company_score
    breakdown["top_companies"] = company_score
    
    # Top Schools (5 points)
    school_score = min(len(signals["top_schools"]) * 2, 5)
    score += school_score
    breakdown["top_schools"] = school_score
    
    # Geography (5 points)
    if signals["geography"] in ["Bangalore", "Mumbai", "Delhi", "Hyderabad"]:
        score += 5
        breakdown["geography"] = 5
    elif signals["geography"]:
        score += 3
        breakdown["geography"] = 3
    else:
        breakdown["geography"] = 0
    
    # Network (5 points)
    network_score = min(len(signals["network"]) * 2, 5)
    score += network_score
    breakdown["network"] = network_score
    
    # Outreach Readiness (5 points)
    if signals["outreach_ready"]:
        score += 5
        breakdown["outreach_ready"] = 5
    else:
        breakdown["outreach_ready"] = 0
    
    # Penalties (up to -20 points)
    penalty_score = min(len(signals["penalties"]) * 5, 20)
    score -= penalty_score
    breakdown["penalties"] = -penalty_score
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    # Determine tier
    if score >= 75:
        tier = "A"
    elif score >= 60:
        tier = "B"
    else:
        tier = "C"
    
    return {
        "total_score": score,
        "tier": tier,
        "breakdown": breakdown,
        "signals": signals
    }

def generate_conversation_starter(profile_data: Dict[str, Any], signals: Dict[str, Any]) -> str:
    """Generate personalized conversation starter"""
    name = profile_data.get("name", "there")
    headline = profile_data.get("headline", "")
    location = profile_data.get("location", "")
    categories = profile_data.get("categories", [])
    
    # Base template
    if "Health" in categories:
        if "AI" in categories:
            template = f"Hi {name}! I noticed you're building in health x AI from {location}. Your background in {headline} caught my attention. Would love to learn more about how you're applying AI to healthcare challenges in India."
        else:
            template = f"Hi {name}! I saw you're working on healthcare solutions from {location}. Your experience in {headline} is exactly what we look for. Open to a quick chat about the healthtech landscape in India?"
    elif "Consumer" in categories:
        if "AI" in categories:
            template = f"Hi {name}! I noticed you're building consumer tech with AI from {location}. Your background in {headline} stood out. Would love to discuss how you're leveraging AI for consumer applications in India."
        else:
            template = f"Hi {name}! I saw you're building consumer tech from {location}. Your experience in {headline} is impressive. Open to a quick chat about the consumer tech opportunity in India?"
    else:
        template = f"Hi {name}! I noticed your work in {headline} from {location}. Your background caught my attention. Would love to learn more about what you're building!"
    
    return template

def main():
    """Main scoring function"""
    print("🎯 Indian Founders Scoring - Health & Consumer Tech")
    print("=" * 60)
    
    # Load filtered profiles
    try:
        with open("indian_founders_filtered.json", "r") as f:
            profiles = json.load(f)
    except FileNotFoundError:
        print("❌ indian_founders_filtered.json not found. Run indian_founders_discovery.py first.")
        return
    
    print(f"📊 Scoring {len(profiles)} Indian founders...")
    
    scored_profiles = []
    tier_counts = {"A": 0, "B": 0, "C": 0}
    category_counts = {}
    
    for profile in profiles:
        # Extract signals
        signals = extract_signals(profile)
        
        # Calculate score
        scoring_result = calculate_score(signals, profile)
        
        # Generate conversation starter
        conversation_starter = generate_conversation_starter(profile, signals)
        
        # Create scored profile
        scored_profile = {
            **profile,
            "score": scoring_result["total_score"],
            "tier": scoring_result["tier"],
            "score_breakdown": scoring_result["breakdown"],
            "signals": signals,
            "conversation_starter": conversation_starter
        }
        
        scored_profiles.append(scored_profile)
        
        # Update counts
        tier_counts[scoring_result["tier"]] += 1
        
        for category in profile.get("categories", []):
            category_counts[category] = category_counts.get(category, 0) + 1
    
    # Sort by score (highest first)
    scored_profiles.sort(key=lambda x: x["score"], reverse=True)
    
    # Save scored profiles
    with open("indian_founders_scored.json", "w") as f:
        json.dump(scored_profiles, f, indent=2)
    
    # Create tier-specific CSV files
    import csv
    
    # All scored profiles
    with open("indian_founders_scored.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "categories", "score", "tier", 
            "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for profile in scored_profiles:
            writer.writerow({
                "name": profile.get("name", ""),
                "headline": profile.get("headline", ""),
                "location": profile.get("location", ""),
                "categories": ", ".join(profile.get("categories", [])),
                "score": profile.get("score", 0),
                "tier": profile.get("tier", ""),
                "conversation_starter": profile.get("conversation_starter", ""),
                "linkedin_url": profile.get("linkedin_url", "")
            })
    
    # Tier A profiles
    tier_a_profiles = [p for p in scored_profiles if p["tier"] == "A"]
    with open("indian_founders_tierA.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "categories", "score", 
            "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for profile in tier_a_profiles:
            writer.writerow({
                "name": profile.get("name", ""),
                "headline": profile.get("headline", ""),
                "location": profile.get("location", ""),
                "categories": ", ".join(profile.get("categories", [])),
                "score": profile.get("score", 0),
                "conversation_starter": profile.get("conversation_starter", ""),
                "linkedin_url": profile.get("linkedin_url", "")
            })
    
    # Tier B profiles
    tier_b_profiles = [p for p in scored_profiles if p["tier"] == "B"]
    with open("indian_founders_tierB.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "categories", "score", 
            "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for profile in tier_b_profiles:
            writer.writerow({
                "name": profile.get("name", ""),
                "headline": profile.get("headline", ""),
                "location": profile.get("location", ""),
                "categories": ", ".join(profile.get("categories", [])),
                "score": profile.get("score", 0),
                "conversation_starter": profile.get("conversation_starter", ""),
                "linkedin_url": profile.get("linkedin_url", "")
            })
    
    # Generate summary
    summary = {
        "total_profiles": len(scored_profiles),
        "tier_distribution": tier_counts,
        "category_distribution": category_counts,
        "average_score": sum(p["score"] for p in scored_profiles) / len(scored_profiles) if scored_profiles else 0,
        "top_locations": {},
        "ai_adoption": {"with_ai": 0, "without_ai": 0}
    }
    
    # Count locations
    for profile in scored_profiles:
        location = profile.get("location", "Unknown")
        summary["top_locations"][location] = summary["top_locations"].get(location, 0) + 1
        
        if profile.get("has_ai"):
            summary["ai_adoption"]["with_ai"] += 1
        else:
            summary["ai_adoption"]["without_ai"] += 1
    
    # Save summary
    with open("indian_founders_scored_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n✅ Scoring Complete!")
    print(f"📊 Total profiles scored: {len(scored_profiles)}")
    print(f"🏆 Tier distribution: {tier_counts}")
    print(f"🏥 Categories: {category_counts}")
    print(f"📍 Top locations: {dict(list(summary['top_locations'].items())[:5])}")
    print(f"🤖 AI adoption: {summary['ai_adoption']}")
    print(f"📈 Average score: {summary['average_score']:.1f}")
    
    print("\n📁 Output files:")
    print("- indian_founders_scored.json: All scored profiles with details")
    print("- indian_founders_scored.csv: All profiles in CSV format")
    print("- indian_founders_tierA.csv: Top tier profiles for immediate outreach")
    print("- indian_founders_tierB.csv: Second tier profiles for targeted outreach")
    print("- indian_founders_scored_summary.json: Summary statistics")

if __name__ == "__main__":
    main()
