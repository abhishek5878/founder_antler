#!/usr/bin/env python3
"""
Real Stealth Founders Search
============================

This script actually searches for real LinkedIn profiles of people
who are genuinely in stealth mode or building something new.
"""

import json
import requests
import time
import re
from typing import List, Dict, Any

def search_real_stealth_profiles() -> List[Dict[str, Any]]:
    """
    Search for real LinkedIn profiles with stealth indicators
    """
    real_profiles = []
    
    # Real search patterns that would find actual stealth founders
    search_queries = [
        # Real stealth indicators
        'site:linkedin.com/in/ "building something"',
        'site:linkedin.com/in/ "stealth mode"',
        'site:linkedin.com/in/ "working on something"',
        'site:linkedin.com/in/ "exploring opportunities"',
        'site:linkedin.com/in/ "recently left" AND "building"',
        'site:linkedin.com/in/ "just left" AND "building"',
        'site:linkedin.com/in/ "transitioning" AND "building"',
        
        # Recent graduates building
        'site:linkedin.com/in/ "2024" AND "building"',
        'site:linkedin.com/in/ "2023" AND "building"',
        'site:linkedin.com/in/ "recent graduate" AND "building"',
        
        # Ex-FAANG building
        'site:linkedin.com/in/ "ex-google" AND "building"',
        'site:linkedin.com/in/ "ex-meta" AND "building"',
        'site:linkedin.com/in/ "ex-amazon" AND "building"',
        'site:linkedin.com/in/ "ex-microsoft" AND "building"',
        'site:linkedin.com/in/ "ex-apple" AND "building"',
        
        # MBA graduates building
        'site:linkedin.com/in/ "MBA" AND "2024" AND "building"',
        'site:linkedin.com/in/ "MBA" AND "2023" AND "building"',
        
        # AI/ML engineers building
        'site:linkedin.com/in/ "ML engineer" AND "building"',
        'site:linkedin.com/in/ "AI engineer" AND "building"',
        'site:linkedin.com/in/ "data scientist" AND "building"',
        
        # YC alumni building new things
        'site:linkedin.com/in/ "YC" AND "building"',
        'site:linkedin.com/in/ "500 startups" AND "building"',
        'site:linkedin.com/in/ "techstars" AND "building"',
        
        # Geographic specific
        'site:linkedin.com/in/ "San Francisco" AND "stealth"',
        'site:linkedin.com/in/ "New York" AND "stealth"',
        'site:linkedin.com/in/ "London" AND "stealth"',
        'site:linkedin.com/in/ "Singapore" AND "stealth"',
        'site:linkedin.com/in/ "Bangalore" AND "stealth"',
        
        # Industry specific
        'site:linkedin.com/in/ "AI" AND "stealth"',
        'site:linkedin.com/in/ "fintech" AND "stealth"',
        'site:linkedin.com/in/ "healthtech" AND "stealth"',
        'site:linkedin.com/in/ "edtech" AND "stealth"',
        'site:linkedin.com/in/ "web3" AND "stealth"',
        
        # PhD students building
        'site:linkedin.com/in/ "PhD" AND "building"',
        'site:linkedin.com/in/ "PhD student" AND "building"',
        'site:linkedin.com/in/ "postdoc" AND "building"',
        
        # Angel investors building
        'site:linkedin.com/in/ "angel investor" AND "building"',
        'site:linkedin.com/in/ "investor" AND "building"',
        
        # Consultants transitioning
        'site:linkedin.com/in/ "ex-mckinsey" AND "building"',
        'site:linkedin.com/in/ "ex-bain" AND "building"',
        'site:linkedin.com/in/ "ex-bcg" AND "building"',
        'site:linkedin.com/in/ "ex-deloitte" AND "building"',
    ]
    
    print(f"🔍 Searching for real stealth profiles using {len(search_queries)} queries...")
    
    for i, query in enumerate(search_queries):
        try:
            print(f"Search {i+1}/{len(search_queries)}: {query[:60]}...")
            
            # Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Extract LinkedIn URLs
                linkedin_pattern = r'https://www\.linkedin\.com/in/[a-zA-Z0-9\-_]+/?'
                matches = re.findall(linkedin_pattern, response.text)
                
                for match in matches:
                    profile_url = match.rstrip('/')
                    
                    # Check if we already have this profile
                    if not any(p.get('url') == profile_url for p in real_profiles):
                        # Create a basic profile entry
                        profile = {
                            "url": profile_url,
                            "name": "Unknown",  # Would need to scrape to get real name
                            "headline": "Unknown",  # Would need to scrape to get real headline
                            "stealth_indicators": [query],
                            "antler_fit_score": 6,  # Default score
                            "key_insights": f"Found via search: {query}",
                            "conversation_starters": [
                                f"Hi! I noticed your profile through a search for {query}. Would love to learn more about what you're building!",
                                "I'm reaching out because I'm interested in connecting with founders building in stealth mode.",
                                "Would love to hear about what you're working on and see if there's potential for collaboration."
                            ]
                        }
                        real_profiles.append(profile)
                
                print(f"✅ Found {len(matches)} profiles")
            else:
                print(f"❌ Search failed: {response.status_code}")
            
            # Rate limiting
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue
    
    return real_profiles

def get_known_real_profiles() -> List[Dict[str, Any]]:
    """
    Return a list of known real profiles that are actually in stealth mode
    These would be profiles we've verified are real and actually building in stealth
    """
    known_profiles = [
        # These would be real profiles we've verified
        # For now, I'll create a template structure
        {
            "url": "https://www.linkedin.com/in/example-real-profile-1/",
            "name": "Real Person 1",
            "headline": "Building something in stealth | Ex-Google Engineer",
            "stealth_indicators": ["building something", "stealth"],
            "antler_fit_score": 8,
            "key_insights": "Real profile found via search",
            "conversation_starters": [
                "Hi! I noticed you're building something in stealth. Would love to learn more!",
                "Your background looks interesting. What are you working on?",
                "Would love to connect and hear about your stealth project."
            ]
        }
    ]
    
    return known_profiles

def main():
    """
    Main execution function
    """
    print("🚀 Real Stealth Founders Search")
    print("=" * 40)
    print("🎯 Searching for real LinkedIn profiles in stealth mode")
    print()
    
    # Search for real profiles
    print("🔍 Step 1: Searching for real stealth profiles...")
    real_profiles = search_real_stealth_profiles()
    
    print(f"\n📊 Found {len(real_profiles)} potential real profiles")
    
    # Save raw search results
    with open("real_stealth_search_results.json", "w") as f:
        json.dump(real_profiles, f, indent=2)
    
    # Generate summary
    summary = {
        "total_profiles_found": len(real_profiles),
        "profiles": real_profiles[:20],  # First 20 profiles
        "search_queries_used": [
            'site:linkedin.com/in/ "building something"',
            'site:linkedin.com/in/ "stealth mode"',
            'site:linkedin.com/in/ "working on something"',
            'site:linkedin.com/in/ "exploring opportunities"',
            'site:linkedin.com/in/ "recently left" AND "building"',
            'site:linkedin.com/in/ "just left" AND "building"',
            'site:linkedin.com/in/ "transitioning" AND "building"',
            'site:linkedin.com/in/ "2024" AND "building"',
            'site:linkedin.com/in/ "2023" AND "building"',
            'site:linkedin.com/in/ "recent graduate" AND "building"',
            'site:linkedin.com/in/ "ex-google" AND "building"',
            'site:linkedin.com/in/ "ex-meta" AND "building"',
            'site:linkedin.com/in/ "ex-amazon" AND "building"',
            'site:linkedin.com/in/ "ex-microsoft" AND "building"',
            'site:linkedin.com/in/ "ex-apple" AND "building"',
            'site:linkedin.com/in/ "MBA" AND "2024" AND "building"',
            'site:linkedin.com/in/ "MBA" AND "2023" AND "building"',
            'site:linkedin.com/in/ "ML engineer" AND "building"',
            'site:linkedin.com/in/ "AI engineer" AND "building"',
            'site:linkedin.com/in/ "data scientist" AND "building"',
            'site:linkedin.com/in/ "YC" AND "building"',
            'site:linkedin.com/in/ "500 startups" AND "building"',
            'site:linkedin.com/in/ "techstars" AND "building"',
            'site:linkedin.com/in/ "San Francisco" AND "stealth"',
            'site:linkedin.com/in/ "New York" AND "stealth"',
            'site:linkedin.com/in/ "London" AND "stealth"',
            'site:linkedin.com/in/ "Singapore" AND "stealth"',
            'site:linkedin.com/in/ "Bangalore" AND "stealth"',
            'site:linkedin.com/in/ "AI" AND "stealth"',
            'site:linkedin.com/in/ "fintech" AND "stealth"',
            'site:linkedin.com/in/ "healthtech" AND "stealth"',
            'site:linkedin.com/in/ "edtech" AND "stealth"',
            'site:linkedin.com/in/ "web3" AND "stealth"',
            'site:linkedin.com/in/ "PhD" AND "building"',
            'site:linkedin.com/in/ "PhD student" AND "building"',
            'site:linkedin.com/in/ "postdoc" AND "building"',
            'site:linkedin.com/in/ "angel investor" AND "building"',
            'site:linkedin.com/in/ "investor" AND "building"',
            'site:linkedin.com/in/ "ex-mckinsey" AND "building"',
            'site:linkedin.com/in/ "ex-bain" AND "building"',
            'site:linkedin.com/in/ "ex-bcg" AND "building"',
            'site:linkedin.com/in/ "ex-deloitte" AND "building"'
        ]
    }
    
    with open("real_stealth_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🎯 Search Complete!")
    print(f"📊 Total profiles found: {len(real_profiles)}")
    
    if real_profiles:
        print(f"\n📋 Sample profiles found:")
        for i, profile in enumerate(real_profiles[:5]):
            print(f"{i+1}. {profile.get('url', 'N/A')}")
            print(f"   Search query: {profile.get('stealth_indicators', ['Unknown'])[0]}")
            print()
    else:
        print("❌ No profiles found - this might be due to rate limiting or search restrictions")
    
    print("📁 Files saved:")
    print("   - real_stealth_search_results.json (raw search results)")
    print("   - real_stealth_summary.json (summary and search queries)")
    
    print(f"\n💡 Next Steps:")
    print("   1. Manually verify the found profiles are real")
    print("   2. Scrape profile details to get names and headlines")
    print("   3. Score profiles based on stealth indicators")
    print("   4. Create personalized conversation starters")

if __name__ == "__main__":
    main()
