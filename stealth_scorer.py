#!/usr/bin/env python3
"""
Stealth Founder Scoring System
Score early-stage stealth founders for Antler conversations
"""

import json
from typing import Dict, Any, List

def score_stealth_founder(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Score a stealth founder based on early-stage indicators"""
    
    # Combine all text fields for analysis
    profile_text = ""
    if profile_data.get('headline'):
        profile_text += profile_data['headline'] + " "
    if profile_data.get('about'):
        profile_text += profile_data['about'] + " "
    if profile_data.get('experience'):
        for exp in profile_data['experience']:
            if isinstance(exp, dict):
                profile_text += exp.get('title', '') + " " + exp.get('company', '') + " "
    if profile_data.get('skills'):
        profile_text += " ".join(profile_data['skills']) + " "
    
    profile_text = profile_text.lower()
    
    # Early-stage stealth indicators (high weight)
    stealth_score = 0
    stealth_indicators = [
        "building something", "building in stealth", "stealth mode", "stealth startup",
        "working on something new", "exploring opportunities", "new opportunity",
        "exciting journey", "next chapter", "starting something new",
        "early stage", "pre-seed", "seed stage", "early-stage",
        "recently joined", "new role", "transitioning", "between opportunities",
        "taking a break", "former", "ex-", "left", "departed"
    ]
    
    for indicator in stealth_indicators:
        if indicator in profile_text:
            stealth_score += 2
    
    # Recent activity indicators (high weight)
    recent_score = 0
    recent_indicators = [
        "2024", "2023", "recent graduate", "recently graduated",
        "new graduate", "fresh graduate", "just graduated",
        "recently joined", "new opportunity", "recent transition"
    ]
    
    for indicator in recent_indicators:
        if indicator in profile_text:
            recent_score += 2
    
    # Background quality indicators (medium weight)
    background_score = 0
    background_indicators = [
        "stanford", "harvard", "mit", "berkeley", "cmu", "caltech",
        "google", "meta", "amazon", "microsoft", "apple", "netflix",
        "mckinsey", "bain", "bcg", "deloitte", "pwc", "ey",
        "phd", "doctorate", "research", "postdoc",
        "software engineer", "ml engineer", "ai researcher", "data scientist",
        "product manager", "technical", "engineering"
    ]
    
    for indicator in background_indicators:
        if indicator in profile_text:
            background_score += 1
    
    # Industry focus indicators (medium weight)
    industry_score = 0
    industry_indicators = [
        "ai", "machine learning", "ml", "artificial intelligence",
        "fintech", "financial technology", "payments", "banking",
        "healthtech", "healthcare", "biotech", "medical",
        "edtech", "education", "learning", "teaching",
        "e-commerce", "marketplace", "retail", "commerce",
        "proptech", "real estate", "property",
        "climate", "sustainability", "green", "renewable",
        "web3", "blockchain", "crypto", "defi", "nft",
        "saas", "software", "platform", "api"
    ]
    
    for indicator in industry_indicators:
        if indicator in profile_text:
            industry_score += 1
    
    # Geographic focus indicators (medium weight)
    geo_score = 0
    geo_indicators = [
        "singapore", "jakarta", "hanoi", "manila", "bangkok", "kuala lumpur",
        "london", "berlin", "stockholm", "amsterdam", "paris", "madrid",
        "nairobi", "lagos", "johannesburg", "accra", "cairo",
        "bangalore", "mumbai", "delhi", "hyderabad", "chennai",
        "sydney", "melbourne", "auckland", "brisbane", "perth",
        "san francisco", "new york", "austin", "toronto", "vancouver"
    ]
    
    for indicator in geo_indicators:
        if indicator in profile_text:
            geo_score += 1
    
    # Accelerator/network indicators (medium weight)
    network_score = 0
    network_indicators = [
        "y combinator", "yc", "500 startups", "techstars", "antler",
        "angel investor", "early stage investor", "venture capital",
        "startup studio", "incubator", "accelerator",
        "sxsw", "techcrunch disrupt", "web summit", "slush"
    ]
    
    for indicator in network_indicators:
        if indicator in profile_text:
            network_score += 1
    
    # Conversation potential indicators (high weight)
    conversation_score = 0
    conversation_indicators = [
        "building", "exploring", "working on", "starting",
        "opportunity", "problem", "solving", "challenge",
        "passionate", "excited", "interested", "curious",
        "learning", "growing", "developing", "creating"
    ]
    
    for indicator in conversation_indicators:
        if indicator in profile_text:
            conversation_score += 1.5
    
    # Calculate weighted total score
    total_score = (
        stealth_score * 0.25 +      # 25% - stealth indicators
        recent_score * 0.20 +       # 20% - recent activity
        background_score * 0.15 +   # 15% - background quality
        industry_score * 0.15 +     # 15% - industry focus
        geo_score * 0.10 +          # 10% - geographic focus
        network_score * 0.10 +      # 10% - network/accelerator
        conversation_score * 0.05   # 5% - conversation potential
    )
    
    # Determine investment readiness
    if total_score >= 8.0:
        investment_readiness = "High"
    elif total_score >= 6.0:
        investment_readiness = "Medium"
    else:
        investment_readiness = "Low"
    
    # Determine market categories
    market_categories = []
    if any(indicator in profile_text for indicator in ["ai", "ml", "machine learning"]):
        market_categories.append("AI/ML")
    if any(indicator in profile_text for indicator in ["fintech", "payments", "banking"]):
        market_categories.append("Fintech")
    if any(indicator in profile_text for indicator in ["healthtech", "healthcare", "biotech"]):
        market_categories.append("Healthtech")
    if any(indicator in profile_text for indicator in ["edtech", "education", "learning"]):
        market_categories.append("Edtech")
    if any(indicator in profile_text for indicator in ["e-commerce", "marketplace", "retail"]):
        market_categories.append("E-commerce")
    if any(indicator in profile_text for indicator in ["proptech", "real estate", "property"]):
        market_categories.append("Proptech")
    if any(indicator in profile_text for indicator in ["climate", "sustainability", "green"]):
        market_categories.append("Climate Tech")
    if any(indicator in profile_text for indicator in ["web3", "blockchain", "crypto"]):
        market_categories.append("Web3/Blockchain")
    
    if not market_categories:
        market_categories.append("Other")
    
    # Determine geographic focus
    geographic_focus = []
    if any(indicator in profile_text for indicator in ["singapore", "jakarta", "hanoi", "manila", "bangkok"]):
        geographic_focus.append("Southeast Asia")
    if any(indicator in profile_text for indicator in ["london", "berlin", "stockholm", "amsterdam", "paris"]):
        geographic_focus.append("Europe")
    if any(indicator in profile_text for indicator in ["nairobi", "lagos", "johannesburg", "accra", "cairo"]):
        geographic_focus.append("Africa")
    if any(indicator in profile_text for indicator in ["bangalore", "mumbai", "delhi", "hyderabad"]):
        geographic_focus.append("India")
    if any(indicator in profile_text for indicator in ["sydney", "melbourne", "auckland"]):
        geographic_focus.append("Australia/NZ")
    if any(indicator in profile_text for indicator in ["san francisco", "new york", "austin", "toronto"]):
        geographic_focus.append("US/Canada")
    
    if not geographic_focus:
        geographic_focus.append("Global")
    
    return {
        "total_score": round(total_score, 2),
        "stealth_score": round(stealth_score, 2),
        "recent_score": round(recent_score, 2),
        "background_score": round(background_score, 2),
        "industry_score": round(industry_score, 2),
        "geo_score": round(geo_score, 2),
        "network_score": round(network_score, 2),
        "conversation_score": round(conversation_score, 2),
        "investment_readiness": investment_readiness,
        "market_categories": market_categories,
        "geographic_focus": geographic_focus,
        "antler_fit": "High" if total_score >= 7.0 else "Medium" if total_score >= 5.0 else "Low"
    }

def create_conversation_starters(profile_data: Dict[str, Any], score_data: Dict[str, Any]) -> List[str]:
    """Create conversation starters for Antler outreach"""
    
    conversation_starters = []
    
    # Get profile text for analysis
    profile_text = ""
    if profile_data.get('headline'):
        profile_text += profile_data['headline'] + " "
    if profile_data.get('about'):
        profile_text += profile_data['about'] + " "
    
    profile_text = profile_text.lower()
    
    # Recent graduate conversation starters
    if any(indicator in profile_text for indicator in ["recent graduate", "2024", "2023", "graduated"]):
        conversation_starters.append(
            "I noticed you recently graduated and are building in [field]. Would love to hear about what you're working on!"
        )
        conversation_starters.append(
            "Your background in [field] is impressive. What's the most exciting problem you're solving right now?"
        )
    
    # Ex-FAANG conversation starters
    if any(indicator in profile_text for indicator in ["ex-google", "ex-meta", "ex-amazon", "ex-microsoft", "ex-apple"]):
        conversation_starters.append(
            "Your experience at [Company] is fascinating. What made you decide to start building something new?"
        )
        conversation_starters.append(
            "I'm curious about your transition from [Company] to building in stealth. What problem are you most excited to solve?"
        )
    
    # Stealth mode conversation starters
    if any(indicator in profile_text for indicator in ["stealth", "building something", "working on"]):
        conversation_starters.append(
            "I see you're building in stealth mode. What's the biggest opportunity you're pursuing?"
        )
        conversation_starters.append(
            "Your stealth project sounds exciting. What problem are you passionate about solving?"
        )
    
    # Industry-specific conversation starters
    if "ai" in profile_text or "ml" in profile_text:
        conversation_starters.append(
            "Your work in AI/ML is fascinating. What's the most exciting application you're building?"
        )
    
    if "fintech" in profile_text or "payments" in profile_text:
        conversation_starters.append(
            "I'm excited about fintech innovation. What opportunity are you most passionate about?"
        )
    
    if "healthtech" in profile_text or "healthcare" in profile_text:
        conversation_starters.append(
            "Healthcare innovation is crucial. What problem are you solving that could make a real impact?"
        )
    
    # Geographic conversation starters
    if any(indicator in profile_text for indicator in ["singapore", "jakarta", "hanoi", "manila", "bangkok"]):
        conversation_starters.append(
            "I'm excited about the Southeast Asia startup ecosystem. What's the biggest opportunity you see there?"
        )
    
    if any(indicator in profile_text for indicator in ["london", "berlin", "stockholm", "amsterdam", "paris"]):
        conversation_starters.append(
            "The European startup scene is growing rapidly. What unique insights do you have about this market?"
        )
    
    # Default conversation starters
    if not conversation_starters:
        conversation_starters.append(
            "I'm excited about what you're building. What's the most interesting problem you're solving?"
        )
        conversation_starters.append(
            "Your background is impressive. What opportunity are you most passionate about pursuing?"
        )
    
    return conversation_starters

def main():
    """Main function"""
    print("🎯 Stealth Founder Scoring System")
    print("=" * 50)
    print("💬 Focus: Score early-stage stealth founders for Antler conversations")
    
    # Sample profile data for demonstration
    sample_profiles = [
        {
            "linkedin": "https://www.linkedin.com/in/anubhab/",
            "headline": "Building AI startup in stealth mode | Ex-Google ML Engineer | Stanford CS 2024",
            "about": "Recent graduate from Stanford building an AI startup in stealth mode. Passionate about solving real-world problems with machine learning.",
            "experience": [
                {"title": "ML Engineer", "company": "Google"},
                {"title": "Software Engineer Intern", "company": "Meta"}
            ],
            "skills": ["Machine Learning", "AI", "Python", "Startup", "Stealth"]
        },
        {
            "linkedin": "https://www.linkedin.com/in/tejasvi-ravi-082b352b/",
            "headline": "Exploring fintech opportunities | Ex-McKinsey | Harvard MBA 2023",
            "about": "Recently graduated from Harvard and exploring fintech opportunities. Building something new in the payments space.",
            "experience": [
                {"title": "Consultant", "company": "McKinsey"},
                {"title": "Product Manager", "company": "Stripe"}
            ],
            "skills": ["Fintech", "Payments", "Strategy", "Product Management"]
        },
        {
            "linkedin": "https://www.linkedin.com/in/sonia-vora-4b321377/",
            "headline": "Building healthtech startup | Ex-Amazon | Berkeley BioE 2024",
            "about": "Recent Berkeley graduate building a healthtech startup. Working on something new in the digital health space.",
            "experience": [
                {"title": "Software Engineer", "company": "Amazon"},
                {"title": "Research Assistant", "company": "UC Berkeley"}
            ],
            "skills": ["Healthtech", "Biotechnology", "Software Engineering", "Research"]
        }
    ]
    
    scored_profiles = []
    
    for profile in sample_profiles:
        score_data = score_stealth_founder(profile)
        conversation_starters = create_conversation_starters(profile, score_data)
        
        scored_profile = {
            "linkedin": profile["linkedin"],
            "headline": profile["headline"],
            "scoring": score_data,
            "conversation_starters": conversation_starters
        }
        
        scored_profiles.append(scored_profile)
    
    # Save scored profiles
    with open('stealth_scored_profiles.json', 'w') as f:
        json.dump(scored_profiles, f, indent=2)
    
    print(f"💾 Scored profiles saved to: stealth_scored_profiles.json")
    
    # Show results
    print(f"\n📊 Scoring Results:")
    for profile in scored_profiles:
        print(f"\n{profile['linkedin']}")
        print(f"Headline: {profile['headline']}")
        print(f"Total Score: {profile['scoring']['total_score']}")
        print(f"Investment Readiness: {profile['scoring']['investment_readiness']}")
        print(f"Antler Fit: {profile['scoring']['antler_fit']}")
        print(f"Market Categories: {', '.join(profile['scoring']['market_categories'])}")
        print(f"Geographic Focus: {', '.join(profile['scoring']['geographic_focus'])}")
        print(f"Conversation Starters:")
        for starter in profile['conversation_starters'][:2]:
            print(f"  - {starter}")
    
    # Create summary
    summary = {
        "total_profiles_scored": len(scored_profiles),
        "scoring_focus": "Early-stage stealth founders for Antler conversations",
        "scoring_criteria": {
            "stealth_score": "25% - stealth indicators",
            "recent_score": "20% - recent activity",
            "background_score": "15% - background quality",
            "industry_score": "15% - industry focus",
            "geo_score": "10% - geographic focus",
            "network_score": "10% - network/accelerator",
            "conversation_score": "5% - conversation potential"
        },
        "next_steps": [
            "1. Apply scoring to real early-stage profiles",
            "2. Filter for high-scoring candidates (7.0+)",
            "3. Use conversation starters for outreach",
            "4. Focus on Antler-fit profiles",
            "5. Prepare personalized messages"
        ]
    }
    
    with open('stealth_scoring_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📋 Summary saved to: stealth_scoring_summary.json")
    
    print(f"\n🎯 Next Steps:")
    print("1. Apply scoring to real early-stage profiles")
    print("2. Filter for high-scoring candidates (7.0+)")
    print("3. Use conversation starters for outreach")
    print("4. Focus on Antler-fit profiles")
    print("5. Prepare personalized messages")

if __name__ == "__main__":
    main()
