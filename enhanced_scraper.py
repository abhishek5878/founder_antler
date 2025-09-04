#!/usr/bin/env python3
"""
Enhanced LinkedIn Profile Scraper
Works with discovered profiles and extracts comprehensive data
"""

import requests
import time
import random
import json
import sys
import argparse
from bs4 import BeautifulSoup
from typing import Dict, List, Any

def scrape_linkedin_profile(url: str) -> Dict[str, Any]:
    """Enhanced LinkedIn profile scraper"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        print(f"🔍 Scraping: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract comprehensive information
            profile_data = {
                'linkedin_url': url,
                'name': extract_name(soup),
                'headline': extract_headline(soup),
                'location': extract_location(soup),
                'summary': extract_summary(soup),
                'experience_data': extract_experience(soup),
                'education_data': extract_education(soup),
                'skills_data': extract_skills(soup),
                'connection_count': extract_connection_count(soup),
                'follower_count': extract_follower_count(soup),
                'achievements': extract_achievements(soup),
                'volunteer_experience': extract_volunteer(soup),
                'certifications': extract_certifications(soup),
                'publications': extract_publications(soup),
                'projects': extract_projects(soup),
                'languages': extract_languages(soup),
                'interests': extract_interests(soup),
                'raw_html': response.text[:1000]  # Store first 1000 chars for debugging
            }
            
            if profile_data['name']:
                print(f"✅ Success: {profile_data['name']}")
                return profile_data
            else:
                print(f"❌ No data extracted from: {url}")
                return {}
        else:
            print(f"❌ HTTP {response.status_code}: {url}")
            return {}
            
    except Exception as e:
        print(f"❌ Error scraping {url}: {str(e)}")
        return {}

def extract_name(soup: BeautifulSoup) -> str:
    """Extract name from LinkedIn profile"""
    selectors = [
        'h1[class*="text-heading"]',
        '.pv-text-details__left-panel h1',
        '.profile-name',
        'h1',
        '.top-card-layout__title',
        '.profile-name',
        '.pv-top-card--name'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            name = element.get_text().strip()
            if name and len(name) > 0:
                return name
    return ""

def extract_headline(soup: BeautifulSoup) -> str:
    """Extract headline from LinkedIn profile"""
    selectors = [
        '.text-body-medium.break-words',
        '.pv-text-details__left-panel .text-body-medium',
        '.profile-headline',
        '.top-card-layout__headline',
        '.pv-top-card--headline',
        '.headline'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            headline = element.get_text().strip()
            if headline and len(headline) > 0:
                return headline
    return ""

def extract_location(soup: BeautifulSoup) -> str:
    """Extract location from LinkedIn profile"""
    selectors = [
        '.text-body-small.inline',
        '.pv-text-details__left-panel .text-body-small',
        '.profile-location',
        '.top-card-layout__location',
        '.pv-top-card--location',
        '.location'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            location = element.get_text().strip()
            if location and len(location) > 0:
                return location
    return ""

def extract_summary(soup: BeautifulSoup) -> str:
    """Extract summary from LinkedIn profile"""
    selectors = [
        '.pv-shared-text-with-see-more',
        '.profile-summary',
        '.about-section',
        '.summary',
        '.pv-about__summary-text',
        '.about'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            summary = element.get_text().strip()
            if summary and len(summary) > 50:  # Only return meaningful summaries
                return summary
    return ""

def extract_experience(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract experience from LinkedIn profile"""
    experiences = []
    
    experience_selectors = [
        '.pv-position-entity',
        '.experience__item',
        '.work-experience',
        '.pv-entity',
        '.experience-item'
    ]
    
    for selector in experience_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:10]:  # Limit to 10 experiences
                try:
                    title = extract_text_from_element(element, ['.pv-entity__name', '.title', 'h3', '.pv-entity__summary-info h3'])
                    company = extract_text_from_element(element, ['.pv-entity__company', '.company', '.organization', '.pv-entity__secondary-title'])
                    duration = extract_text_from_element(element, ['.pv-entity__date-range', '.duration', '.time-period'])
                    location = extract_text_from_element(element, ['.pv-entity__location', '.location'])
                    description = extract_text_from_element(element, ['.pv-entity__description', '.description', '.summary'])
                    
                    if title or company:
                        experiences.append({
                            'title': title,
                            'company': company,
                            'duration': duration,
                            'location': location,
                            'description': description
                        })
                except:
                    continue
            break
    
    return experiences

def extract_education(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract education from LinkedIn profile"""
    education = []
    
    education_selectors = [
        '.pv-education-entity',
        '.education__item',
        '.education',
        '.pv-entity'
    ]
    
    for selector in education_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:5]:  # Limit to 5 education entries
                try:
                    institution = extract_text_from_element(element, ['.pv-entity__school-name', '.school', '.institution', '.pv-entity__summary-info h3'])
                    degree = extract_text_from_element(element, ['.pv-entity__degree-name', '.degree', '.field', '.pv-entity__secondary-title'])
                    field = extract_text_from_element(element, ['.pv-entity__field-of-study', '.field-of-study'])
                    year = extract_text_from_element(element, ['.pv-entity__dates', '.year', '.graduation-year'])
                    
                    if institution or degree:
                        education.append({
                            'institution': institution,
                            'degree': degree,
                            'field': field,
                            'year': year
                        })
                except:
                    continue
            break
    
    return education

def extract_skills(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract skills from LinkedIn profile"""
    skills = []
    
    skill_selectors = [
        '.pv-skill-category-entity',
        '.skill-item',
        '.skill',
        '.pv-skill-category-entity__name'
    ]
    
    for selector in skill_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:15]:  # Limit to 15 skills
                try:
                    skill_name = extract_text_from_element(element, ['.pv-skill-category-entity__name', '.skill-name', '.name'])
                    endorsement_count = extract_endorsements(element)
                    
                    if skill_name:
                        skills.append({
                            'skill': skill_name,
                            'endorsement_count': endorsement_count
                        })
                except:
                    continue
            break
    
    return skills

def extract_connection_count(soup: BeautifulSoup) -> int:
    """Extract connection count"""
    connection_selectors = [
        '.pv-top-card--list-bullet .pv-top-card--list-bullet',
        '.connection-count',
        '.connections',
        '.pv-top-card--list-bullet'
    ]
    
    for selector in connection_selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text().strip()
            import re
            numbers = re.findall(r'\d+', text.replace(',', ''))
            if numbers:
                return int(numbers[0])
    return 0

def extract_follower_count(soup: BeautifulSoup) -> int:
    """Extract follower count"""
    follower_selectors = [
        '.pv-top-card--list-bullet .pv-top-card--list-bullet:nth-child(2)',
        '.follower-count',
        '.followers'
    ]
    
    for selector in follower_selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text().strip()
            import re
            numbers = re.findall(r'\d+', text.replace(',', ''))
            if numbers:
                return int(numbers[0])
    return 0

def extract_achievements(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract achievements and awards"""
    achievements = []
    
    achievement_selectors = [
        '.pv-accomplishment-entity',
        '.achievement',
        '.award'
    ]
    
    for selector in achievement_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:5]:
                try:
                    title = extract_text_from_element(element, ['.pv-accomplishment-entity__title', '.title'])
                    issuer = extract_text_from_element(element, ['.pv-accomplishment-entity__issuer', '.issuer'])
                    year = extract_text_from_element(element, ['.pv-accomplishment-entity__year', '.year'])
                    
                    if title:
                        achievements.append({
                            'title': title,
                            'issuer': issuer,
                            'year': year
                        })
                except:
                    continue
            break
    
    return achievements

def extract_volunteer(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract volunteer experience"""
    volunteer = []
    
    volunteer_selectors = [
        '.pv-volunteering-entity',
        '.volunteer'
    ]
    
    for selector in volunteer_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:3]:
                try:
                    title = extract_text_from_element(element, ['.pv-volunteering-entity__role', '.title'])
                    organization = extract_text_from_element(element, ['.pv-volunteering-entity__organization', '.organization'])
                    duration = extract_text_from_element(element, ['.pv-volunteering-entity__date-range', '.duration'])
                    
                    if title or organization:
                        volunteer.append({
                            'title': title,
                            'organization': organization,
                            'duration': duration
                        })
                except:
                    continue
            break
    
    return volunteer

def extract_certifications(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract certifications"""
    certifications = []
    
    cert_selectors = [
        '.pv-certification-entity',
        '.certification'
    ]
    
    for selector in cert_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:5]:
                try:
                    name = extract_text_from_element(element, ['.pv-certification-entity__name', '.name'])
                    issuer = extract_text_from_element(element, ['.pv-certification-entity__issuer', '.issuer'])
                    year = extract_text_from_element(element, ['.pv-certification-entity__year', '.year'])
                    
                    if name:
                        certifications.append({
                            'name': name,
                            'issuer': issuer,
                            'year': year
                        })
                except:
                    continue
            break
    
    return certifications

def extract_publications(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract publications"""
    publications = []
    
    pub_selectors = [
        '.pv-publication-entity',
        '.publication'
    ]
    
    for selector in pub_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:3]:
                try:
                    title = extract_text_from_element(element, ['.pv-publication-entity__title', '.title'])
                    publisher = extract_text_from_element(element, ['.pv-publication-entity__publisher', '.publisher'])
                    year = extract_text_from_element(element, ['.pv-publication-entity__year', '.year'])
                    
                    if title:
                        publications.append({
                            'title': title,
                            'publisher': publisher,
                            'year': year
                        })
                except:
                    continue
            break
    
    return publications

def extract_projects(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract projects"""
    projects = []
    
    project_selectors = [
        '.pv-project-entity',
        '.project'
    ]
    
    for selector in project_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:3]:
                try:
                    title = extract_text_from_element(element, ['.pv-project-entity__title', '.title'])
                    description = extract_text_from_element(element, ['.pv-project-entity__description', '.description'])
                    year = extract_text_from_element(element, ['.pv-project-entity__year', '.year'])
                    
                    if title:
                        projects.append({
                            'title': title,
                            'description': description,
                            'year': year
                        })
                except:
                    continue
            break
    
    return projects

def extract_languages(soup: BeautifulSoup) -> List[str]:
    """Extract languages"""
    languages = []
    
    lang_selectors = [
        '.pv-accomplishment-entity__title',
        '.language'
    ]
    
    for selector in lang_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements:
                text = element.get_text().strip()
                if text and len(text) < 50:  # Likely a language name
                    languages.append(text)
    
    return languages[:5]  # Limit to 5 languages

def extract_interests(soup: BeautifulSoup) -> List[str]:
    """Extract interests"""
    interests = []
    
    interest_selectors = [
        '.pv-interest-entity__name',
        '.interest'
    ]
    
    for selector in interest_selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements[:10]:
                text = element.get_text().strip()
                if text:
                    interests.append(text)
    
    return interests

def extract_endorsements(element) -> int:
    """Extract endorsement count from skill element"""
    try:
        endorsement_selectors = [
            '.pv-skill-category-entity__endorsement-count',
            '.endorsement-count'
        ]
        
        for selector in endorsement_selectors:
            endorsement_element = element.select_one(selector)
            if endorsement_element:
                text = endorsement_element.get_text().strip()
                import re
                numbers = re.findall(r'\d+', text.replace(',', ''))
                if numbers:
                    return int(numbers[0])
    except:
        pass
    return 0

def extract_text_from_element(element, selectors: List[str]) -> str:
    """Extract text from element using multiple selectors"""
    for selector in selectors:
        try:
            found_element = element.select_one(selector)
            if found_element:
                text = found_element.get_text().strip()
                if text:
                    return text
        except:
            continue
    return ""

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Enhanced LinkedIn Profile Scraper')
    parser.add_argument('--profiles', type=str, help='JSON file with profile URLs')
    parser.add_argument('--limit', type=int, default=50, help='Maximum number of profiles to scrape')
    args = parser.parse_args()
    
    print("🚀 Enhanced LinkedIn Profile Scraper")
    print("=" * 50)
    
    # Load profiles to scrape
    if args.profiles:
        try:
            with open(args.profiles, 'r') as f:
                profile_urls = json.load(f)
            print(f"📁 Loaded {len(profile_urls)} profiles from {args.profiles}")
        except FileNotFoundError:
            print(f"❌ File not found: {args.profiles}")
            return
    else:
        # Default test URLs
        profile_urls = [
            "https://www.linkedin.com/in/anubhab/",
            "https://www.linkedin.com/in/tejasvi-ravi-082b352b/",
            "https://www.linkedin.com/in/sonia-vora-4b321377/",
            "https://www.linkedin.com/in/sanjeevsrinivasan07/",
            "https://www.linkedin.com/in/pskumar2018/"
        ]
        print("📁 Using default test profiles")
    
    # Limit number of profiles
    profile_urls = profile_urls[:args.limit]
    
    results = []
    
    for i, url in enumerate(profile_urls, 1):
        print(f"\n{i}/{len(profile_urls)}: {url}")
        
        profile_data = scrape_linkedin_profile(url)
        if profile_data:
            results.append(profile_data)
        
        # Random delay to be respectful
        time.sleep(random.uniform(2, 4))
    
    print("\n" + "=" * 50)
    print("SCRAPING RESULTS")
    print("=" * 50)
    print(f"Total URLs tested: {len(profile_urls)}")
    print(f"Successfully extracted: {len(results)}")
    print(f"Success rate: {len(results)/len(profile_urls)*100:.1f}%")
    
    if results:
        print("\nExtracted Profiles:")
        for i, profile in enumerate(results, 1):
            print(f"\n{i}. {profile['name']}")
            print(f"   Headline: {profile.get('headline', 'N/A')}")
            print(f"   Location: {profile.get('location', 'N/A')}")
            print(f"   Experience: {len(profile.get('experience_data', []))} entries")
            print(f"   Education: {len(profile.get('education_data', []))} entries")
            print(f"   Skills: {len(profile.get('skills_data', []))} skills")
            print(f"   Achievements: {len(profile.get('achievements', []))} awards")
    
    # Save results
    if results:
        with open('enhanced_scraped_profiles.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Enhanced results saved to: enhanced_scraped_profiles.json")

if __name__ == "__main__":
    main()
