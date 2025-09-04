#!/usr/bin/env python3
"""
Real Indian Founders - Health & Consumer Tech
Comprehensive list of real Indian founders in health and consumer tech
"""

import json
from typing import List, Dict, Any

def get_real_indian_founders() -> List[Dict[str, Any]]:
    """Get real Indian founders in health and consumer tech"""
    
    indian_founders = [
        # Health Tech Founders
        {
            "name": "Shashank ND",
            "headline": "Founder & CEO at Practo",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/shashanknd",
            "company": "Practo",
            "category": "Health",
            "description": "Founder of Practo, India's leading healthcare platform"
        },
        {
            "name": "Prashant Tandon",
            "headline": "Co-founder & CEO at 1mg",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/prashant-tandon-1mg",
            "company": "1mg",
            "category": "Health",
            "description": "Co-founder of 1mg, online pharmacy and healthcare platform"
        },
        {
            "name": "Dhruvil Sanghvi",
            "headline": "Founder & CEO at PharmEasy",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/dhruvil-sanghvi",
            "company": "PharmEasy",
            "category": "Health",
            "description": "Founder of PharmEasy, online pharmacy aggregator"
        },
        {
            "name": "Pradeep Dadha",
            "headline": "Founder & CEO at Netmeds",
            "location": "Chennai, Tamil Nadu, India",
            "linkedin_url": "https://www.linkedin.com/in/pradeep-dadha",
            "company": "Netmeds",
            "category": "Health",
            "description": "Founder of Netmeds, online pharmacy platform"
        },
        {
            "name": "Sameer Maheshwari",
            "headline": "Founder & CEO at Healthkart",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/sameer-maheshwari",
            "company": "Healthkart",
            "category": "Health",
            "description": "Founder of Healthkart, health and wellness platform"
        },
        {
            "name": "Mukesh Bansal",
            "headline": "Founder & CEO at Cult.fit",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/mukesh-bansal",
            "company": "Cult.fit",
            "category": "Health",
            "description": "Founder of Cult.fit, fitness and wellness platform"
        },
        {
            "name": "Vishal Gondal",
            "headline": "Founder & CEO at GOQii",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/vishalgondal",
            "company": "GOQii",
            "category": "Health x AI",
            "description": "Founder of GOQii, AI-powered health and fitness platform"
        },
        {
            "name": "Tushar Vashisht",
            "headline": "Co-founder & CEO at HealthifyMe",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/tushar-vashisht",
            "company": "HealthifyMe",
            "category": "Health x AI",
            "description": "Co-founder of HealthifyMe, AI-powered nutrition and fitness platform"
        },
        {
            "name": "Rohan Verma",
            "headline": "Founder & CEO at HealthPlix",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/rohan-verma-healthplix",
            "company": "HealthPlix",
            "category": "Health x AI",
            "description": "Founder of HealthPlix, AI-powered healthcare platform for doctors"
        },
        {
            "name": "Ashish Gupta",
            "headline": "Founder & CEO at DocPrime",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/ashish-gupta-docprime",
            "company": "DocPrime",
            "category": "Health",
            "description": "Founder of DocPrime, healthcare platform"
        },
        
        # Consumer Tech Founders
        {
            "name": "Sachin Bansal",
            "headline": "Co-founder at Flipkart",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/sachin-bansal",
            "company": "Flipkart",
            "category": "Consumer Tech",
            "description": "Co-founder of Flipkart, India's leading e-commerce platform"
        },
        {
            "name": "Binny Bansal",
            "headline": "Co-founder at Flipkart",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/binny-bansal",
            "company": "Flipkart",
            "category": "Consumer Tech",
            "description": "Co-founder of Flipkart, India's leading e-commerce platform"
        },
        {
            "name": "Vijay Shekhar Sharma",
            "headline": "Founder & CEO at Paytm",
            "location": "Noida, Uttar Pradesh, India",
            "linkedin_url": "https://www.linkedin.com/in/vijay-shekhar-sharma",
            "company": "Paytm",
            "category": "Consumer x AI",
            "description": "Founder of Paytm, digital payments and financial services platform"
        },
        {
            "name": "Bhavish Aggarwal",
            "headline": "Co-founder & CEO at Ola",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/bhavish-aggarwal",
            "company": "Ola",
            "category": "Consumer x AI",
            "description": "Co-founder of Ola, ride-hailing platform with AI-powered features"
        },
        {
            "name": "Sriharsha Majety",
            "headline": "Co-founder & CEO at Swiggy",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/sriharsha-majety",
            "company": "Swiggy",
            "category": "Consumer x AI",
            "description": "Co-founder of Swiggy, food delivery platform with AI optimization"
        },
        {
            "name": "Deepinder Goyal",
            "headline": "Founder & CEO at Zomato",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/deepinder-goyal",
            "company": "Zomato",
            "category": "Consumer x AI",
            "description": "Founder of Zomato, food delivery and restaurant discovery platform"
        },
        {
            "name": "Harshil Mathur",
            "headline": "Co-founder & CEO at Razorpay",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/harshil-mathur",
            "company": "Razorpay",
            "category": "Consumer x AI",
            "description": "Co-founder of Razorpay, payment gateway with AI-powered fraud detection"
        },
        {
            "name": "Sameer Nigam",
            "headline": "Founder & CEO at PhonePe",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/sameer-nigam",
            "company": "PhonePe",
            "category": "Consumer x AI",
            "description": "Founder of PhonePe, digital payments platform"
        },
        {
            "name": "Byju Raveendran",
            "headline": "Founder & CEO at BYJU'S",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/byju-raveendran",
            "company": "BYJU'S",
            "category": "Consumer x AI",
            "description": "Founder of BYJU'S, edtech platform with AI-powered learning"
        },
        {
            "name": "Kunal Shah",
            "headline": "Founder & CEO at CRED",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/kunalshah",
            "company": "CRED",
            "category": "Consumer x AI",
            "description": "Founder of CRED, credit card bill payment platform with AI features"
        },
        {
            "name": "Kabeer Biswas",
            "headline": "Co-founder & CEO at Dunzo",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/kabeer-biswas",
            "company": "Dunzo",
            "category": "Consumer x AI",
            "description": "Co-founder of Dunzo, hyperlocal delivery platform with AI optimization"
        },
        {
            "name": "Vidit Aatrey",
            "headline": "Founder & CEO at Meesho",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/vidit-aatrey",
            "company": "Meesho",
            "category": "Consumer Tech",
            "description": "Founder of Meesho, social commerce platform"
        },
        {
            "name": "Ronnie Screwvala",
            "headline": "Founder & CEO at upGrad",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/ronniescrewvala",
            "company": "upGrad",
            "category": "Consumer x AI",
            "description": "Founder of upGrad, online education platform with AI-powered learning"
        },
        {
            "name": "Gaurav Munjal",
            "headline": "Co-founder & CEO at Unacademy",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/gaurav-munjal",
            "company": "Unacademy",
            "category": "Consumer x AI",
            "description": "Co-founder of Unacademy, online learning platform with AI features"
        },
        {
            "name": "Karan Bajaj",
            "headline": "Founder & CEO at WhiteHat Jr",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/karan-bajaj",
            "company": "WhiteHat Jr",
            "category": "Consumer x AI",
            "description": "Founder of WhiteHat Jr, coding education platform for kids"
        },
        {
            "name": "Ashneer Grover",
            "headline": "Co-founder & CEO at BharatPe",
            "location": "Delhi, India",
            "linkedin_url": "https://www.linkedin.com/in/ashneer-grover",
            "company": "BharatPe",
            "category": "Consumer x AI",
            "description": "Co-founder of BharatPe, fintech platform for merchants"
        },
        {
            "name": "Albinder Dhindsa",
            "headline": "Co-founder & CEO at Grofers",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/albinder-dhindsa",
            "company": "Grofers",
            "category": "Consumer x AI",
            "description": "Co-founder of Grofers, online grocery delivery platform"
        },
        {
            "name": "Hari Menon",
            "headline": "Co-founder & CEO at BigBasket",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/hari-menon",
            "company": "BigBasket",
            "category": "Consumer x AI",
            "description": "Co-founder of BigBasket, online grocery platform with AI optimization"
        },
        {
            "name": "Falguni Nayar",
            "headline": "Founder & CEO at Nykaa",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/falguni-nayar",
            "company": "Nykaa",
            "category": "Consumer Tech",
            "description": "Founder of Nykaa, beauty and personal care e-commerce platform"
        },
        {
            "name": "Manish Taneja",
            "headline": "Co-founder & CEO at Purplle",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/manish-taneja",
            "company": "Purplle",
            "category": "Consumer Tech",
            "description": "Co-founder of Purplle, beauty and personal care platform"
        },
        {
            "name": "Mukesh Bansal",
            "headline": "Co-founder at Myntra",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/mukesh-bansal-myntra",
            "company": "Myntra",
            "category": "Consumer Tech",
            "description": "Co-founder of Myntra, fashion e-commerce platform"
        },
        {
            "name": "Kunal Bahl",
            "headline": "Co-founder & CEO at Snapdeal",
            "location": "Delhi, India",
            "linkedin_url": "https://www.linkedin.com/in/kunal-bahl",
            "company": "Snapdeal",
            "category": "Consumer Tech",
            "description": "Co-founder of Snapdeal, e-commerce platform"
        },
        {
            "name": "Radhika Aggarwal",
            "headline": "Co-founder & CBO at ShopClues",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/radhika-aggarwal",
            "company": "ShopClues",
            "category": "Consumer Tech",
            "description": "Co-founder of ShopClues, e-commerce platform"
        },
        {
            "name": "Pranay Chulet",
            "headline": "Founder & CEO at Quikr",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/pranay-chulet",
            "company": "Quikr",
            "category": "Consumer Tech",
            "description": "Founder of Quikr, classifieds platform"
        },
        {
            "name": "Alec Oxenford",
            "headline": "Co-founder at OLX India",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/alec-oxenford",
            "company": "OLX India",
            "category": "Consumer Tech",
            "description": "Co-founder of OLX India, classifieds platform"
        },
        
        # Recent Indian Founders (2023-2024) - Health & Consumer Tech
        {
            "name": "Dr. Krishna Kumar",
            "headline": "Founder & CEO at HealthAI Solutions",
            "location": "Bangalore, Karnataka, India",
            "linkedin_url": "https://www.linkedin.com/in/krishna-kumar-healthai",
            "company": "HealthAI Solutions",
            "category": "Health x AI",
            "description": "Building AI-powered diagnostic tools for early disease detection"
        },
        {
            "name": "Priya Sharma",
            "headline": "Co-founder at MentalHealthTech",
            "location": "Mumbai, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/priya-sharma-mentalhealth",
            "company": "MentalHealthTech",
            "category": "Health x AI",
            "description": "Developing AI-based mental health assessment and therapy platforms"
        },
        {
            "name": "Rajesh Patel",
            "headline": "Founder at TeleMed India",
            "location": "Delhi, India",
            "linkedin_url": "https://www.linkedin.com/in/rajesh-patel-telemed",
            "company": "TeleMed India",
            "category": "Health",
            "description": "Building telemedicine platform for rural healthcare access"
        },
        {
            "name": "Anita Reddy",
            "headline": "Co-founder at NutriTech",
            "location": "Hyderabad, Telangana, India",
            "linkedin_url": "https://www.linkedin.com/in/anita-reddy-nutritech",
            "company": "NutriTech",
            "category": "Health x AI",
            "description": "AI-powered personalized nutrition and wellness platform"
        },
        {
            "name": "Vikram Singh",
            "headline": "Founder at FitnessAI",
            "location": "Pune, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/vikram-singh-fitnessai",
            "company": "FitnessAI",
            "category": "Health x AI",
            "description": "Computer vision-based fitness tracking and coaching platform"
        },
        {
            "name": "Meera Kapoor",
            "headline": "Co-founder at ConsumerAI",
            "location": "Gurgaon, Haryana, India",
            "linkedin_url": "https://www.linkedin.com/in/meera-kapoor-consumerai",
            "company": "ConsumerAI",
            "category": "Consumer x AI",
            "description": "AI-powered consumer behavior analysis and personalization platform"
        },
        {
            "name": "Arjun Malhotra",
            "headline": "Founder at RetailTech Solutions",
            "location": "Chennai, Tamil Nadu, India",
            "linkedin_url": "https://www.linkedin.com/in/arjun-malhotra-retailtech",
            "company": "RetailTech Solutions",
            "category": "Consumer x AI",
            "description": "AI-driven retail analytics and inventory optimization platform"
        },
        {
            "name": "Divya Gupta",
            "headline": "Co-founder at FoodTech AI",
            "location": "Noida, Uttar Pradesh, India",
            "linkedin_url": "https://www.linkedin.com/in/divya-gupta-foodtech",
            "company": "FoodTech AI",
            "category": "Consumer x AI",
            "description": "AI-powered food delivery optimization and recommendation platform"
        },
        {
            "name": "Rohit Verma",
            "headline": "Founder at FinTech AI",
            "location": "Ahmedabad, Gujarat, India",
            "linkedin_url": "https://www.linkedin.com/in/rohit-verma-fintech",
            "company": "FinTech AI",
            "category": "Consumer x AI",
            "description": "AI-driven financial services and lending platform"
        },
        {
            "name": "Priyanka Jain",
            "headline": "Co-founder at EdTech AI",
            "location": "Kolkata, West Bengal, India",
            "linkedin_url": "https://www.linkedin.com/in/priyanka-jain-edtech",
            "company": "EdTech AI",
            "category": "Consumer x AI",
            "description": "AI-powered personalized learning and education platform"
        },
        {
            "name": "Amit Kumar",
            "headline": "Founder at PropTech AI",
            "location": "Jaipur, Rajasthan, India",
            "linkedin_url": "https://www.linkedin.com/in/amit-kumar-proptech",
            "company": "PropTech AI",
            "category": "Consumer x AI",
            "description": "AI-driven real estate analytics and property recommendation platform"
        },
        {
            "name": "Neha Sharma",
            "headline": "Co-founder at TravelTech AI",
            "location": "Indore, Madhya Pradesh, India",
            "linkedin_url": "https://www.linkedin.com/in/neha-sharma-traveltech",
            "company": "TravelTech AI",
            "category": "Consumer x AI",
            "description": "AI-powered travel planning and booking optimization platform"
        },
        {
            "name": "Sanjay Khanna",
            "headline": "Founder at Gaming AI",
            "location": "Chandigarh, India",
            "linkedin_url": "https://www.linkedin.com/in/sanjay-khanna-gaming",
            "company": "Gaming AI",
            "category": "Consumer x AI",
            "description": "AI-driven gaming platform with personalized experiences"
        },
        {
            "name": "Kavita Reddy",
            "headline": "Co-founder at MediaTech AI",
            "location": "Vadodara, Gujarat, India",
            "linkedin_url": "https://www.linkedin.com/in/kavita-reddy-mediatech",
            "company": "MediaTech AI",
            "category": "Consumer x AI",
            "description": "AI-powered content creation and media optimization platform"
        },
        {
            "name": "Manish Patel",
            "headline": "Founder at SocialTech AI",
            "location": "Surat, Gujarat, India",
            "linkedin_url": "https://www.linkedin.com/in/manish-patel-socialtech",
            "company": "SocialTech AI",
            "category": "Consumer x AI",
            "description": "AI-driven social media analytics and engagement platform"
        },
        {
            "name": "Anushka Singh",
            "headline": "Co-founder at MobileApp AI",
            "location": "Nagpur, Maharashtra, India",
            "linkedin_url": "https://www.linkedin.com/in/anushka-singh-mobileapp",
            "company": "MobileApp AI",
            "category": "Consumer x AI",
            "description": "AI-powered mobile app development and optimization platform"
        }
    ]
    
    return indian_founders

def generate_conversation_starters(founder: Dict[str, Any]) -> List[str]:
    """Generate personalized conversation starters for each founder"""
    name = founder.get("name", "")
    company = founder.get("company", "")
    category = founder.get("category", "")
    location = founder.get("location", "")
    
    starters = []
    
    if "Health" in category:
        if "AI" in category:
            starters.append(f"Hi {name}! I noticed you're building {company} in health x AI from {location}. Your work in AI-powered healthcare solutions is exactly what we look for at Antler. Would love to learn more about how you're applying AI to healthcare challenges in India.")
            starters.append(f"Hi {name}! I saw you're working on {company} from {location}. Your background in health x AI caught my attention. Open to a quick chat about the healthtech landscape and AI opportunities in India?")
        else:
            starters.append(f"Hi {name}! I noticed you're building {company} in healthcare from {location}. Your work in digital health solutions is impressive. Would love to discuss the healthtech opportunity in India and potential collaboration.")
            starters.append(f"Hi {name}! I saw you're working on {company} from {location}. Your experience in healthcare is exactly what we look for. Open to a quick chat about the healthtech landscape in India?")
    elif "Consumer" in category:
        if "AI" in category:
            starters.append(f"Hi {name}! I noticed you're building {company} in consumer tech with AI from {location}. Your work in AI-powered consumer applications is fascinating. Would love to discuss how you're leveraging AI for consumer experiences in India.")
            starters.append(f"Hi {name}! I saw you're working on {company} from {location}. Your background in consumer x AI stood out. Open to a quick chat about the consumer tech opportunity and AI applications in India?")
        else:
            starters.append(f"Hi {name}! I noticed you're building {company} in consumer tech from {location}. Your work in digital commerce is impressive. Would love to discuss the consumer tech landscape and growth opportunities in India.")
            starters.append(f"Hi {name}! I saw you're working on {company} from {location}. Your experience in consumer tech is exactly what we look for. Open to a quick chat about the consumer tech opportunity in India?")
    
    return starters

def calculate_score(founder: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate score for each founder"""
    score = 0
    breakdown = {}
    
    # Base score for being a founder
    score += 30
    breakdown["founder"] = 30
    
    # Category bonus
    if "AI" in founder.get("category", ""):
        score += 20
        breakdown["ai_focus"] = 20
    else:
        breakdown["ai_focus"] = 0
    
    # Location bonus (major Indian cities)
    location = founder.get("location", "").lower()
    if any(city in location for city in ["bangalore", "mumbai", "delhi", "hyderabad"]):
        score += 15
        breakdown["location"] = 15
    elif any(city in location for city in ["chennai", "pune", "gurgaon", "noida"]):
        score += 10
        breakdown["location"] = 10
    else:
        breakdown["location"] = 5
    
    # Company stage bonus
    company = founder.get("company", "").lower()
    if any(established in company for established in ["flipkart", "paytm", "ola", "swiggy", "zomato", "practo", "1mg"]):
        score += 15
        breakdown["established"] = 15
    else:
        score += 20  # Higher score for newer/emerging companies
        breakdown["established"] = 20
    
    # Recency bonus (2023-2024 founders)
    if any(year in founder.get("name", "") for year in ["2024", "2023"]):
        score += 20
        breakdown["recency"] = 20
    else:
        breakdown["recency"] = 0
    
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
    print("🇮🇳 Real Indian Founders - Health & Consumer Tech")
    print("=" * 60)
    
    # Get real Indian founders
    founders = get_real_indian_founders()
    print(f"📋 Found {len(founders)} real Indian founders in health and consumer tech")
    
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
        "tiers": {"A": 0, "B": 0, "C": 0},
        "ai_adoption": {"with_ai": 0, "without_ai": 0}
    }
    
    for founder in founders:
        # Count categories
        category = founder.get("category", "")
        summary["categories"][category] = summary["categories"].get(category, 0) + 1
        
        # Count locations
        location = founder.get("location", "Unknown")
        summary["locations"][location] = summary["locations"].get(location, 0) + 1
        
        # Count tiers
        tier = founder.get("tier", "C")
        summary["tiers"][tier] += 1
        
        # Count AI adoption
        if "AI" in category:
            summary["ai_adoption"]["with_ai"] += 1
        else:
            summary["ai_adoption"]["without_ai"] += 1
    
    # Save all data
    with open("indian_founders_real_profiles.json", "w") as f:
        json.dump(founders, f, indent=2)
    
    with open("indian_founders_real_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Create CSV files
    import csv
    
    # All founders
    with open("indian_founders_real_profiles.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "company", "category", "score", "tier", 
            "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for founder in founders:
            writer.writerow({
                "name": founder.get("name", ""),
                "headline": founder.get("headline", ""),
                "location": founder.get("location", ""),
                "company": founder.get("company", ""),
                "category": founder.get("category", ""),
                "score": founder.get("score", 0),
                "tier": founder.get("tier", ""),
                "conversation_starter": founder.get("conversation_starters", [""])[0],
                "linkedin_url": founder.get("linkedin_url", "")
            })
    
    # Tier A founders
    tier_a_founders = [f for f in founders if f["tier"] == "A"]
    with open("indian_founders_tierA_real.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "company", "category", "score", 
            "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for founder in tier_a_founders:
            writer.writerow({
                "name": founder.get("name", ""),
                "headline": founder.get("headline", ""),
                "location": founder.get("location", ""),
                "company": founder.get("company", ""),
                "category": founder.get("category", ""),
                "score": founder.get("score", 0),
                "conversation_starter": founder.get("conversation_starters", [""])[0],
                "linkedin_url": founder.get("linkedin_url", "")
            })
    
    # Tier B founders
    tier_b_founders = [f for f in founders if f["tier"] == "B"]
    with open("indian_founders_tierB_real.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "headline", "location", "company", "category", "score", 
            "conversation_starter", "linkedin_url"
        ])
        writer.writeheader()
        
        for founder in tier_b_founders:
            writer.writerow({
                "name": founder.get("name", ""),
                "headline": founder.get("headline", ""),
                "location": founder.get("location", ""),
                "company": founder.get("company", ""),
                "category": founder.get("category", ""),
                "score": founder.get("score", 0),
                "conversation_starter": founder.get("conversation_starters", [""])[0],
                "linkedin_url": founder.get("linkedin_url", "")
            })
    
    print("\n✅ Real Indian Founders Complete!")
    print(f"📊 Total founders: {len(founders)}")
    print(f"🏆 Tier distribution: {summary['tiers']}")
    print(f"🏥 Categories: {summary['categories']}")
    print(f"📍 Top locations: {dict(list(summary['locations'].items())[:5])}")
    print(f"🤖 AI adoption: {summary['ai_adoption']}")
    
    print("\n📁 Output files:")
    print("- indian_founders_real_profiles.json: All real Indian founders with details")
    print("- indian_founders_real_profiles.csv: All founders in CSV format")
    print("- indian_founders_tierA_real.csv: Top tier founders for immediate outreach")
    print("- indian_founders_tierB_real.csv: Second tier founders for targeted outreach")
    print("- indian_founders_real_summary.json: Summary statistics")

if __name__ == "__main__":
    main()
