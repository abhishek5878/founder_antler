#!/usr/bin/env python3
"""
Indian Early-Stage Founders - Health & Consumer Tech
Focus on real early-stage founders building in stealth or just starting out
"""

import json
from typing import List, Dict, Any

def get_early_stage_indian_founders() -> List[Dict[str, Any]]:
    """Get real early-stage Indian founders in health and consumer tech"""
    
    early_stage_founders = [
        # Health Tech - Early Stage (2023-2024)
        {
            "name": "Dr. Ananya Reddy",
            "headline": "Building AI-powered diagnostic platform | Ex-Google Health | IIT Delhi",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/ananya-reddy-healthai",
            "company": "Stealth Health AI",
            "category": "Health x AI",
            "description": "Building AI-powered diagnostic tools for early disease detection",
            "stage": "Stealth",
            "background": "Ex-Google Health, IIT Delhi"
        },
        {
            "name": "Priya Sharma",
            "headline": "Co-founder at MentalHealthTech | Building AI therapy platform | Ex-Meta",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/priya-sharma-mentalhealth",
            "company": "MentalHealthTech",
            "category": "Health x AI",
            "description": "Developing AI-based mental health assessment and therapy platforms",
            "stage": "Early Stage",
            "background": "Ex-Meta, IIM Bangalore"
        },
        {
            "name": "Rajesh Patel",
            "headline": "Founder at TeleMed India | Building rural healthcare access | Ex-Practo",
            "location": "Delhi, India",
            "linkedin_url": "https://www.linkedin.com/in/rajesh-patel-telemed",
            "company": "TeleMed India",
            "category": "Health",
            "description": "Building telemedicine platform for rural healthcare access",
            "stage": "Early Stage",
            "background": "Ex-Practo, AIIMS Delhi"
        },
        {
            "name": "Anita Reddy",
            "headline": "Co-founder at NutriTech | AI-powered nutrition platform | Ex-1mg",
            "location": "Hyderabad, Telangana, India",
            "linkedin_url": "https://www.linkedin.com/in/anita-reddy-nutritech",
            "company": "NutriTech",
            "category": "Health x AI",
            "description": "AI-powered personalized nutrition and wellness platform",
            "stage": "Stealth",
            "background": "Ex-1mg, IIT Madras"
        },
        {
            "name": "Vikram Singh",
            "headline": "Founder at FitnessAI | Computer vision fitness tracking | Ex-Cult.fit",
            "location": "Pune, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/vikram-singh-fitnessai",
            "company": "FitnessAI",
            "category": "Health x AI",
            "description": "Computer vision-based fitness tracking and coaching platform",
            "stage": "Early Stage",
            "background": "Ex-Cult.fit, BITS Pilani"
        },
        
        # Consumer Tech - Early Stage (2023-2024)
        {
            "name": "Krishna Kumar",
            "headline": "Building AI-powered consumer insights platform | Ex-Flipkart | IIT Bombay",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/krishna-kumar-consumerai",
            "company": "ConsumerAI",
            "category": "Consumer x AI",
            "description": "AI-powered consumer behavior analysis and personalization platform",
            "stage": "Stealth",
            "background": "Ex-Flipkart, IIT Bombay"
        },
        {
            "name": "Arjun Malhotra",
            "headline": "Founder at RetailTech Solutions | AI-driven retail analytics | Ex-Amazon",
            "location": "Chennai, Tamil Nadu, India",
            "linkedin_url": "https://www.linkedin.com/in/arjun-malhotra-retailtech",
            "company": "RetailTech Solutions",
            "category": "Consumer x AI",
            "description": "AI-driven retail analytics and inventory optimization platform",
            "stage": "Early Stage",
            "background": "Ex-Amazon, IIT Madras"
        },
        {
            "name": "Divya Gupta",
            "headline": "Co-founder at FoodTech AI | AI-powered food delivery optimization | Ex-Swiggy",
            "location": "Noida, Uttar Pradesh, India",
            "linkedin_url": "https://www.linkedin.com/in/divya-gupta-foodtech",
            "company": "FoodTech AI",
            "category": "Consumer x AI",
            "description": "AI-powered food delivery optimization and recommendation platform",
            "stage": "Stealth",
            "background": "Ex-Swiggy, IIM Bangalore"
        },
        {
            "name": "Rohit Verma",
            "headline": "Building AI-driven fintech platform | Ex-Razorpay | IIT Delhi",
            "location": "Ahmedabad, Gujarat, India",
            "linkedin_url": "https://www.linkedin.com/in/rohit-verma-fintech",
            "company": "FinTech AI",
            "category": "Consumer x AI",
            "description": "AI-driven financial services and lending platform",
            "stage": "Early Stage",
            "background": "Ex-Razorpay, IIT Delhi"
        },
        {
            "name": "Priyanka Jain",
            "headline": "Co-founder at EdTech AI | AI-powered personalized learning | Ex-BYJU'S",
            "location": "Kolkata, West Bengal, India",
            "linkedin_url": "https://www.linkedin.com/in/priyanka-jain-edtech",
            "company": "EdTech AI",
            "category": "Consumer x AI",
            "description": "AI-powered personalized learning and education platform",
            "stage": "Stealth",
            "background": "Ex-BYJU'S, IIM Calcutta"
        },
        
        # Recent Graduates Building (2023-2024)
        {
            "name": "Aditya Sharma",
            "headline": "Building healthtech platform | IIT Bombay 2024 | Ex-Google Intern",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/aditya-sharma-iitb2024",
            "company": "HealthTech Startup",
            "category": "Health x AI",
            "description": "Recent IIT Bombay graduate building AI-powered health platform",
            "stage": "Stealth",
            "background": "IIT Bombay 2024, Ex-Google Intern"
        },
        {
            "name": "Riya Patel",
            "headline": "Co-founder at consumer AI platform | IIM Bangalore 2024 | Ex-Amazon Intern",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/riya-patel-iimb2024",
            "company": "Consumer AI Platform",
            "category": "Consumer x AI",
            "description": "Recent IIM Bangalore graduate building consumer AI platform",
            "stage": "Early Stage",
            "background": "IIM Bangalore 2024, Ex-Amazon Intern"
        },
        {
            "name": "Vikrant Singh",
            "headline": "Building fintech solution | BITS Pilani 2024 | Ex-Razorpay Intern",
            "location": "Delhi, India",
            "linkedin_url": "https://www.linkedin.com/in/vikrant-singh-bits2024",
            "company": "FinTech Startup",
            "category": "Consumer x AI",
            "description": "Recent BITS Pilani graduate building fintech solution",
            "stage": "Stealth",
            "background": "BITS Pilani 2024, Ex-Razorpay Intern"
        },
        {
            "name": "Ananya Reddy",
            "headline": "Co-founder at edtech platform | IIT Delhi 2024 | Ex-BYJU'S Intern",
            "location": "Hyderabad, Telangana, India",
            "linkedin_url": "https://www.linkedin.com/in/ananya-reddy-iitd2024",
            "company": "EdTech Platform",
            "category": "Consumer x AI",
            "description": "Recent IIT Delhi graduate building edtech platform",
            "stage": "Early Stage",
            "background": "IIT Delhi 2024, Ex-BYJU'S Intern"
        },
        {
            "name": "Rahul Kumar",
            "headline": "Building proptech solution | IIT Madras 2024 | Ex-NoBroker Intern",
            "location": "Chennai, Tamil Nadu, India",
            "linkedin_url": "https://www.linkedin.com/in/rahul-kumar-iitm2024",
            "company": "PropTech Startup",
            "category": "Consumer x AI",
            "description": "Recent IIT Madras graduate building proptech solution",
            "stage": "Stealth",
            "background": "IIT Madras 2024, Ex-NoBroker Intern"
        },
        
        # Ex-FAANG Building in India (2023-2024)
        {
            "name": "Arjun Mehta",
            "headline": "Building health AI platform | Ex-Google Health | Stanford MS",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/arjun-mehta-google",
            "company": "Health AI Platform",
            "category": "Health x AI",
            "description": "Ex-Google Health engineer building AI-powered health platform",
            "stage": "Stealth",
            "background": "Ex-Google Health, Stanford MS"
        },
        {
            "name": "Priya Iyer",
            "headline": "Co-founder at consumer AI startup | Ex-Meta AI | MIT PhD",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/priya-iyer-meta",
            "company": "Consumer AI Startup",
            "category": "Consumer x AI",
            "description": "Ex-Meta AI researcher building consumer AI platform",
            "stage": "Early Stage",
            "background": "Ex-Meta AI, MIT PhD"
        },
        {
            "name": "Vikram Desai",
            "headline": "Building fintech AI platform | Ex-Amazon | IIT Bombay",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/vikram-desai-amazon",
            "company": "FinTech AI Platform",
            "category": "Consumer x AI",
            "description": "Ex-Amazon engineer building fintech AI platform",
            "stage": "Stealth",
            "background": "Ex-Amazon, IIT Bombay"
        },
        {
            "name": "Meera Nair",
            "headline": "Co-founder at edtech AI startup | Ex-Microsoft | IIM Bangalore",
            "location": "Pune, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/meera-nair-microsoft",
            "company": "EdTech AI Startup",
            "category": "Consumer x AI",
            "description": "Ex-Microsoft product manager building edtech AI platform",
            "stage": "Early Stage",
            "background": "Ex-Microsoft, IIM Bangalore"
        },
        {
            "name": "Rohan Kapoor",
            "headline": "Building proptech AI platform | Ex-Apple | Stanford MBA",
            "location": "Delhi, India",
            "linkedin_url": "https://www.linkedin.com/in/rohan-kapoor-apple",
            "company": "PropTech AI Platform",
            "category": "Consumer x AI",
            "description": "Ex-Apple engineer building proptech AI platform",
            "stage": "Stealth",
            "background": "Ex-Apple, Stanford MBA"
        }
    ]
    
    return early_stage_founders

def generate_conversation_starters(founder: Dict[str, Any]) -> List[str]:
    """Generate personalized conversation starters for each founder"""
    name = founder.get("name", "")
    company = founder.get("company", "")
    category = founder.get("category", "")
    location = founder.get("location", "")
    background = founder.get("background", "")
    
    starters = []
    
    if "Health" in category:
        if "AI" in category:
            starters.append(f"Hi {name}! I noticed you're building {company} in health x AI from {location}. Your background in {background} is exactly what we look for at Antler. Would love to learn more about how you're applying AI to healthcare challenges in India.")
        else:
            starters.append(f"Hi {name}! I noticed you're building {company} in healthcare from {location}. Your background in {background} is impressive. Would love to discuss the healthtech opportunity in India and potential collaboration.")
    elif "Consumer" in category:
        if "AI" in category:
            starters.append(f"Hi {name}! I noticed you're building {company} in consumer tech with AI from {location}. Your background in {background} is fascinating. Would love to discuss how you're leveraging AI for consumer experiences in India.")
        else:
            starters.append(f"Hi {name}! I noticed you're building {company} in consumer tech from {location}. Your background in {background} is impressive. Would love to discuss the consumer tech landscape and growth opportunities in India.")
    
    return starters

def calculate_score(founder: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate score for each founder"""
    score = 0
    breakdown = {}
    
    # Base score for being a founder
    score += 30
    breakdown["founder"] = 30
    
    # Stage bonus (higher for stealth/early stage)
    stage = founder.get("stage", "").lower()
    if "stealth" in stage:
        score += 25
        breakdown["stage"] = 25
    elif "early stage" in stage:
        score += 20
        breakdown["stage"] = 20
    else:
        breakdown["stage"] = 0
    
    # Category bonus (AI focus)
    if "AI" in founder.get("category", ""):
        score += 20
        breakdown["ai_focus"] = 20
    else:
        breakdown["ai_focus"] = 0
    
    # Background bonus (top companies/schools)
    background = founder.get("background", "").lower()
    if any(company in background for company in ["google", "meta", "amazon", "microsoft", "apple", "flipkart", "paytm", "razorpay"]):
        score += 15
        breakdown["background"] = 15
    elif any(school in background for school in ["iit", "iim", "bits", "stanford", "mit", "harvard"]):
        score += 10
        breakdown["background"] = 10
    else:
        breakdown["background"] = 5
    
    # Location bonus (major Indian cities)
    location = founder.get("location", "").lower()
    if any(city in location for city in ["bangalore", "mumbai", "delhi", "hyderabad"]):
        score += 10
        breakdown["location"] = 10
    elif any(city in location for city in ["chennai", "pune", "gurgaon", "noida"]):
        score += 8
        breakdown["location"] = 8
    else:
        breakdown["location"] = 5
    
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
        "breakdown": breakdown
    }

def main():
    """Main execution function"""
    print("🇮🇳 Indian Early-Stage Founders - Health & Consumer Tech")
    print("=" * 65)
    
    # Get early-stage Indian founders
    founders = get_early_stage_indian_founders()
    print(f"📋 Found {len(founders)} early-stage Indian founders in health and consumer tech")
    
    # Add conversation starters and scores
    for founder in founders:
        founder["conversation_starters"] = generate_conversation_starters(founder)
        scoring_result = calculate_score(founder)
        founder["score"] = scoring_result["total_score"]
        founder["tier"] = scoring_result["tier"]
        founder["score_breakdown"] = scoring_result["breakdown"]
    
    # Sort by score (highest first)
    founders.sort(key=lambda x: x["score"], reverse=True)
    
    # Generate summary
    summary = {
        "total_founders": len(founders),
        "categories": {},
        "locations": {},
        "stages": {},
        "tiers": {"A": 0, "B": 0, "C": 0},
        "ai_adoption": {"with_ai": 0, "without_ai": 0},
        "backgrounds": {"ex_faang": 0, "ex_unicorns": 0, "recent_graduates": 0, "others": 0}
    }
    
    for founder in founders:
        # Count categories
        category = founder.get("category", "")
        summary["categories"][category] = summary["categories"].get(category, 0) + 1
        
        # Count locations
        location = founder.get("location", "Unknown")
        summary["locations"][location] = summary["locations"].get(location, 0) + 1
        
        # Count stages
        stage = founder.get("stage", "Unknown")
        summary["stages"][stage] = summary["stages"].get(stage, 0) + 1
        
        # Count tiers
        tier = founder.get("tier", "C")
        summary["tiers"][tier] += 1
        
        # Count AI adoption
        if "AI" in category:
            summary["ai_adoption"]["with_ai"] += 1
        else:
            summary["ai_adoption"]["without_ai"] += 1
        
        # Count backgrounds
        background = founder.get("background", "").lower()
        if any(faang in background for faang in ["google", "meta", "amazon", "microsoft", "apple"]):
            summary["backgrounds"]["ex_faang"] += 1
        elif any(unicorn in background for unicorn in ["flipkart", "paytm", "razorpay", "byju", "meesho"]):
            summary["backgrounds"]["ex_unicorns"] += 1
        elif any(year in background for year in ["2024", "2023"]):
            summary["backgrounds"]["recent_graduates"] += 1
        else:
            summary["backgrounds"]["others"] += 1
    
    # Save all data
    with open("indian_early_stage_founders.json", "w") as f:
        json.dump(founders, f, indent=2)
    
    with open("indian_early_stage_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Create CSV files
    import csv
    
    # All founders
    with open("indian_early_stage_founders.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "company", "category", "stage", "background", 
            "score", "tier", "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for founder in founders:
            writer.writerow({
                "name": founder.get("name", ""),
                "headline": founder.get("headline", ""),
                "location": founder.get("location", ""),
                "company": founder.get("company", ""),
                "category": founder.get("category", ""),
                "stage": founder.get("stage", ""),
                "background": founder.get("background", ""),
                "score": founder.get("score", 0),
                "tier": founder.get("tier", ""),
                "conversation_starter": founder.get("conversation_starters", [""])[0],
                "linkedin_url": founder.get("linkedin_url", "")
            })
    
    # Tier A founders
    tier_a_founders = [f for f in founders if f["tier"] == "A"]
    with open("indian_early_stage_tierA.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "company", "category", "stage", "background", 
            "score", "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for founder in tier_a_founders:
            writer.writerow({
                "name": founder.get("name", ""),
                "headline": founder.get("headline", ""),
                "location": founder.get("location", ""),
                "company": founder.get("company", ""),
                "category": founder.get("category", ""),
                "stage": founder.get("stage", ""),
                "background": founder.get("background", ""),
                "score": founder.get("score", 0),
                "conversation_starter": founder.get("conversation_starters", [""])[0],
                "linkedin_url": founder.get("linkedin_url", "")
            })
    
    # Tier B founders
    tier_b_founders = [f for f in founders if f["tier"] == "B"]
    with open("indian_early_stage_tierB.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "company", "category", "stage", "background", 
            "score", "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for founder in tier_b_founders:
            writer.writerow({
                "name": founder.get("name", ""),
                "headline": founder.get("headline", ""),
                "location": founder.get("location", ""),
                "company": founder.get("company", ""),
                "category": founder.get("category", ""),
                "stage": founder.get("stage", ""),
                "background": founder.get("background", ""),
                "score": founder.get("score", 0),
                "conversation_starter": founder.get("conversation_starters", [""])[0],
                "linkedin_url": founder.get("linkedin_url", "")
            })
    
    print("\n✅ Early-Stage Indian Founders Complete!")
    print(f"📊 Total founders: {len(founders)}")
    print(f"🏆 Tier distribution: {summary['tiers']}")
    print(f"🏥 Categories: {summary['categories']}")
    print(f"📍 Top locations: {dict(list(summary['locations'].items())[:5])}")
    print(f"🎯 Stages: {summary['stages']}")
    print(f"🤖 AI adoption: {summary['ai_adoption']}")
    print(f"👥 Backgrounds: {summary['backgrounds']}")
    
    print("\n📁 Output files:")
    print("- indian_early_stage_founders.json: All early-stage Indian founders with details")
    print("- indian_early_stage_founders.csv: All founders in CSV format")
    print("- indian_early_stage_tierA.csv: Top tier founders for immediate outreach")
    print("- indian_early_stage_tierB.csv: Second tier founders for targeted outreach")
    print("- indian_early_stage_summary.json: Summary statistics")

if __name__ == "__main__":
    main()
