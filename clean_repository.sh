#!/bin/bash

echo "🧹 Cleaning up repository - keeping only essential files..."

# Files to KEEP (essential for the stealth founder discovery system)
ESSENTIAL_FILES=(
    # Core scripts
    "real_early_stage_founders.py"
    "stealth_scorer.py"
    "enhanced_scraper.py"
    
    # Data files
    "real_early_stage_founders.json"
    "stealth_scored_profiles.json"
    "stealth_conversation_starters.json"
    
    # Documentation
    "README.md"
    "STEALTH_FOUNDERS_FINAL_SUMMARY.md"
    "requirements.txt"
    "env_example.txt"
    
    # Configuration
    ".gitignore"
    "config.py"
    
    # Setup scripts
    "setup_github_repo.sh"
    "push_to_github.sh"
    "clean_repository.sh"
)

# Files to REMOVE (unnecessary or redundant)
FILES_TO_REMOVE=(
    # Old/experimental scripts
    "actual_stealth_founders.py"
    "actual_stealth_founders.json"
    "actual_stealth_criteria.json"
    "actual_stealth_summary.json"
    "curated_stealth_founders.py"
    "curated_stealth_founders.json"
    "curated_stealth_summary.json"
    "stealth_founders_discovery.py"
    "stealth_founders_profiles.json"
    "stealth_founders_summary.json"
    "stealth_founders_criteria.json"
    "real_stealth_founders.py"
    "real_linkedin_profiles.py"
    "real_linkedin_profiles.json"
    "real_profiles_summary.json"
    "early_stage_stealth_founders.py"
    
    # Antler-specific files (redundant)
    "antler_complete_data.json"
    "antler_comprehensive_analysis.json"
    "antler_comprehensive.py"
    "antler_discovered_profiles.json"
    "antler_founder_discovery.py"
    "antler_portfolio_founders.py"
    "antler_real_profiles.py"
    "antler_scored_demo.json"
    "antler_scorer.py"
    "antler_scoring_system.py"
    "ANTLER_FOUNDER_SOURCING_SUMMARY.md"
    "comprehensive_antler_profiles.json"
    
    # Old/experimental files
    "100_plus_founders_plan.json"
    "complete_five_profiles.py"
    "complete_five_profiles.json"
    "complete_five_summary.json"
    "comprehensive_profiles.json"
    "comprehensive_summary.json"
    "discovered_100_plus_profiles.json"
    "discovered_profiles.json"
    "enhanced_scraped_profiles.json"
    "execute_antler_plan.py"
    "find_profiles.py"
    "firecrawl_scraper.py"
    "generate_100_plus_profiles.py"
    "get_fifth_profile.py"
    "implementation_plan.json"
    "linkedin_scraper.py"
    "main.py"
    "manual_profiles.json"
    "models.py"
    "profile_discovery.py"
    "profile_summary.json"
    "robust_scraped_profiles.json"
    "robust_scraper.py"
    "run_next_phase.py"
    "scored_profiles.json"
    "scoring_engine.py"
    "scraped_profiles.json"
    "simple_pipeline.py"
    "simple_scoring.py"
    "simple_scraper.py"
    "ultimate_scraper.py"
    
    # Old documentation
    "FINAL_ANTLER_ACCOMPLISHMENT.md"
    "FINAL_SUMMARY.md"
    "REAL_LINKEDIN_PROFILES_ACCOMPLISHMENT.md"
    
    # Old automation
    "automation_pipeline.py"
    "dashboard.py"
    "data_processor.py"
)

echo "📁 Files to keep (${#ESSENTIAL_FILES[@]} files):"
for file in "${ESSENTIAL_FILES[@]}"; do
    echo "  ✅ $file"
done

echo ""
echo "🗑️ Files to remove (${#FILES_TO_REMOVE[@]} files):"
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "  ❌ $file"
    fi
done

echo ""
echo "🚀 Starting cleanup..."

# Remove unnecessary files
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "Removing: $file"
        rm "$file"
    fi
done

echo ""
echo "✅ Cleanup complete!"
echo "📊 Remaining files:"
ls -la | grep -E "\.(py|json|md|txt|sh)$" | wc -l

echo ""
echo "🎯 Essential files remaining:"
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
    fi
done
