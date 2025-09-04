#!/usr/bin/env python3
"""
Real Profile Discovery using Firecrawl + OpenAI
==============================================

This script uses Firecrawl to scrape LinkedIn profiles and OpenAI to analyze
and find similar real profiles that Antler can reach out to.
"""

import os
import json
import time
import requests
from typing import List, Dict, Any
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure APIs
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Sample profiles to base discovery on
SAMPLE_PROFILES = [
    "https://www.linkedin.com/in/anubhab/",
    "https://www.linkedin.com/in/tejasvi-ravi-082b352b/", 
    "https://www.linkedin.com/in/sonia-vora-4b321377/",
    "https://www.linkedin.com/in/sanjeevsrinivasan07/",
    "https://www.linkedin.com/in/pskumar2018/"
]

def scrape_linkedin_profile(profile_url: str) -> Dict[str, Any]:
    """
    Scrape a LinkedIn profile using Firecrawl API
    """
    try:
        url = "https://api.firecrawl.dev/scrape"
        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": profile_url,
            "includeHtml": True,
            "waitFor": 3000
        }
        
        print(f"🔍 Scraping: {profile_url}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "url": profile_url,
                "success": True,
                "data": data.get("data", {}),
                "html": data.get("html", "")
            }
        else:
            print(f"❌ Failed to scrape {profile_url}: {response.status_code}")
            return {"url": profile_url, "success": False, "error": response.text}
            
    except Exception as e:
        print(f"❌ Error scraping {profile_url}: {str(e)}")
        return {"url": profile_url, "success": False, "error": str(e)}

def analyze_profile_with_openai(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use OpenAI to analyze a profile and extract key information
    """
    try:
        # Extract text content from profile
        content = profile_data.get("data", {}).get("markdown", "")
        if not content:
            return {"success": False, "error": "No content to analyze"}
        
        # Create prompt for OpenAI
        prompt = f"""
        Analyze this LinkedIn profile and extract key information for Antler VC:
        
        Profile Content:
        {content[:2000]}  # Limit content length
        
        Please extract and return a JSON object with:
        {{
            "name": "Full name",
            "headline": "Current headline/role",
            "location": "Location",
            "current_company": "Current company/project",
            "background": "Key previous companies (max 3)",
            "education": "Education background",
            "skills": ["skill1", "skill2", "skill3"],
            "stealth_indicators": ["indicator1", "indicator2"],
            "antler_fit_score": 1-10,
            "investment_readiness": "High/Medium/Low",
            "conversation_potential": "High/Medium/Low",
            "key_insights": "Brief analysis for Antler"
        }}
        
        Focus on:
        - Early-stage indicators (recent graduates, stealth mode, building something)
        - AI/ML, fintech, healthtech backgrounds
        - Geographic fit for Antler locations
        - Conversation potential for Antler team
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a VC analyst helping Antler find early-stage founders. Extract key information from LinkedIn profiles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse JSON response
        analysis_text = response.choices[0].message.content
        try:
            analysis = json.loads(analysis_text)
            analysis["success"] = True
            return analysis
        except json.JSONDecodeError:
            return {"success": False, "error": "Failed to parse OpenAI response"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def find_similar_profiles_with_openai(sample_profiles: List[Dict[str, Any]]) -> List[str]:
    """
    Use OpenAI to generate search queries to find similar profiles
    """
    try:
        # Create a summary of sample profiles
        profile_summary = []
        for profile in sample_profiles:
            if profile.get("success") and profile.get("analysis", {}).get("success"):
                analysis = profile["analysis"]
                profile_summary.append({
                    "headline": analysis.get("headline", ""),
                    "background": analysis.get("background", ""),
                    "skills": analysis.get("skills", []),
                    "stealth_indicators": analysis.get("stealth_indicators", [])
                })
        
        prompt = f"""
        Based on these sample LinkedIn profiles, generate 20 specific LinkedIn search queries to find similar early-stage founders:
        
        Sample Profiles:
        {json.dumps(profile_summary, indent=2)}
        
        Generate search queries that will find real LinkedIn profiles of:
        - Recent graduates (2023-2024) building startups
        - Ex-FAANG employees who recently left to build something
        - People with "stealth", "building", "exploring" in their headlines
        - Founders with AI/ML, fintech, healthtech backgrounds
        - People in Antler locations (US, Europe, Asia, Africa)
        
        Return as JSON array of search strings:
        [
            "site:linkedin.com/in/ \"building something\" AND (founder OR co-founder)",
            "site:linkedin.com/in/ \"stealth mode\" AND (AI OR ML OR fintech)",
            ...
        ]
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a search expert helping find early-stage founders on LinkedIn."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        search_queries_text = response.choices[0].message.content
        try:
            search_queries = json.loads(search_queries_text)
            return search_queries
        except json.JSONDecodeError:
            print("❌ Failed to parse search queries")
            return []
            
    except Exception as e:
        print(f"❌ Error generating search queries: {str(e)}")
        return []

def search_google_for_profiles(search_queries: List[str]) -> List[str]:
    """
    Search Google for LinkedIn profiles using the generated queries
    """
    discovered_profiles = set()
    
    for i, query in enumerate(search_queries[:10]):  # Limit to first 10 queries
        try:
            print(f"🔍 Search {i+1}/{len(search_queries)}: {query}")
            
            # Use Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Extract LinkedIn URLs from search results
                import re
                linkedin_pattern = r'https://www\.linkedin\.com/in/[a-zA-Z0-9\-_]+/?'
                matches = re.findall(linkedin_pattern, response.text)
                
                for match in matches:
                    profile_url = match.rstrip('/')
                    if profile_url not in SAMPLE_PROFILES:
                        discovered_profiles.add(profile_url)
                
                print(f"✅ Found {len(matches)} LinkedIn profiles")
            else:
                print(f"❌ Search failed: {response.status_code}")
            
            # Rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error searching: {str(e)}")
            continue
    
    return list(discovered_profiles)

def main():
    """
    Main execution function
    """
    print("🚀 Real Profile Discovery for Antler")
    print("=" * 50)
    print("🎯 Using Firecrawl + OpenAI to find real early-stage founders")
    print()
    
    # Step 1: Scrape sample profiles
    print("📊 Step 1: Analyzing sample profiles...")
    sample_analyses = []
    
    for profile_url in SAMPLE_PROFILES:
        # Scrape profile
        profile_data = scrape_linkedin_profile(profile_url)
        
        if profile_data["success"]:
            # Analyze with OpenAI
            analysis = analyze_profile_with_openai(profile_data)
            sample_analyses.append({
                "url": profile_url,
                "data": profile_data,
                "analysis": analysis
            })
            
            if analysis.get("success"):
                print(f"✅ {profile_url}")
                print(f"   Name: {analysis.get('name', 'N/A')}")
                print(f"   Headline: {analysis.get('headline', 'N/A')}")
                print(f"   Antler Fit: {analysis.get('antler_fit_score', 'N/A')}/10")
            else:
                print(f"❌ Analysis failed: {analysis.get('error', 'Unknown error')}")
        else:
            print(f"❌ Scraping failed: {profile_data.get('error', 'Unknown error')}")
        
        time.sleep(1)  # Rate limiting
    
    # Step 2: Generate search queries
    print("\n🔍 Step 2: Generating search queries...")
    search_queries = find_similar_profiles_with_openai(sample_analyses)
    print(f"✅ Generated {len(search_queries)} search queries")
    
    # Step 3: Search for similar profiles
    print("\n🌐 Step 3: Searching for similar profiles...")
    discovered_profiles = search_google_for_profiles(search_queries)
    print(f"✅ Discovered {len(discovered_profiles)} potential profiles")
    
    # Step 4: Analyze discovered profiles
    print("\n📊 Step 4: Analyzing discovered profiles...")
    final_profiles = []
    
    for i, profile_url in enumerate(discovered_profiles[:20]):  # Limit to first 20
        print(f"Analyzing {i+1}/{min(20, len(discovered_profiles))}: {profile_url}")
        
        # Scrape profile
        profile_data = scrape_linkedin_profile(profile_url)
        
        if profile_data["success"]:
            # Analyze with OpenAI
            analysis = analyze_profile_with_openai(profile_data)
            
            if analysis.get("success"):
                final_profiles.append({
                    "url": profile_url,
                    "analysis": analysis
                })
                
                print(f"   ✅ {analysis.get('name', 'N/A')} - {analysis.get('headline', 'N/A')}")
                print(f"   Antler Fit: {analysis.get('antler_fit_score', 'N/A')}/10")
            else:
                print(f"   ❌ Analysis failed")
        else:
            print(f"   ❌ Scraping failed")
        
        time.sleep(1)  # Rate limiting
    
    # Step 5: Save results
    print("\n💾 Step 5: Saving results...")
    
    # Save discovered profiles
    with open("real_discovered_profiles.json", "w") as f:
        json.dump(discovered_profiles, f, indent=2)
    
    # Save analyzed profiles
    with open("real_analyzed_profiles.json", "w") as f:
        json.dump(final_profiles, f, indent=2)
    
    # Save sample analyses
    with open("sample_profile_analyses.json", "w") as f:
        json.dump(sample_analyses, f, indent=2)
    
    # Generate summary
    summary = {
        "total_discovered": len(discovered_profiles),
        "total_analyzed": len(final_profiles),
        "high_fit_profiles": len([p for p in final_profiles if p["analysis"].get("antler_fit_score", 0) >= 7]),
        "medium_fit_profiles": len([p for p in final_profiles if 4 <= p["analysis"].get("antler_fit_score", 0) < 7]),
        "low_fit_profiles": len([p for p in final_profiles if p["analysis"].get("antler_fit_score", 0) < 4]),
        "top_profiles": sorted(final_profiles, key=lambda x: x["analysis"].get("antler_fit_score", 0), reverse=True)[:10]
    }
    
    with open("discovery_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🎯 Discovery Complete!")
    print(f"📊 Total profiles discovered: {len(discovered_profiles)}")
    print(f"📊 Profiles analyzed: {len(final_profiles)}")
    print(f"🎯 High fit profiles (7+): {summary['high_fit_profiles']}")
    print(f"📈 Medium fit profiles (4-6): {summary['medium_fit_profiles']}")
    print(f"📉 Low fit profiles (<4): {summary['low_fit_profiles']}")
    
    print(f"\n🏆 Top 5 Profiles for Antler:")
    for i, profile in enumerate(summary["top_profiles"][:5]):
        analysis = profile["analysis"]
        print(f"{i+1}. {analysis.get('name', 'N/A')}")
        print(f"   {analysis.get('headline', 'N/A')}")
        print(f"   Antler Fit: {analysis.get('antler_fit_score', 'N/A')}/10")
        print(f"   {analysis.get('key_insights', 'N/A')}")
        print()
    
    print("📁 Files saved:")
    print("   - real_discovered_profiles.json (all discovered URLs)")
    print("   - real_analyzed_profiles.json (analyzed profiles)")
    print("   - sample_profile_analyses.json (sample profile analysis)")
    print("   - discovery_summary.json (summary statistics)")

if __name__ == "__main__":
    main()
