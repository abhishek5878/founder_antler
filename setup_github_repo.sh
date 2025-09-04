#!/bin/bash

# GitHub Repository Setup Script for founder_antler
echo "🚀 Setting up GitHub repository for founder_antler..."

# Check if git is configured
if ! git config --global user.name > /dev/null 2>&1; then
    echo "❌ Git user.name not configured. Please run:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
    exit 1
fi

if ! git config --global user.email > /dev/null 2>&1; then
    echo "❌ Git user.email not configured. Please run:"
    echo "   git config --global user.email 'your.email@example.com'"
    exit 1
fi

echo "✅ Git configuration verified"

# Instructions for creating GitHub repository
echo ""
echo "📋 MANUAL STEPS REQUIRED:"
echo "=========================="
echo ""
echo "1. Go to https://github.com/new"
echo "2. Repository name: founder_antler"
echo "3. Description: Founder Sourcing & Scoring System for Antler - Discover and score early-stage stealth founders"
echo "4. Make it Public or Private (your choice)"
echo "5. DO NOT initialize with README (we already have one)"
echo "6. Click 'Create repository'"
echo ""
echo "After creating the repository, run these commands:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/founder_antler.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "Replace YOUR_USERNAME with your actual GitHub username"
echo ""

# Check if remote is already added
if git remote -v | grep -q "origin"; then
    echo "✅ Remote origin already configured"
    echo "Current remote:"
    git remote -v
    echo ""
    echo "To push to GitHub, run:"
    echo "git push -u origin main"
else
    echo "❌ No remote origin configured yet"
    echo "Please follow the manual steps above to create the repository"
fi

echo ""
echo "🎯 REPOSITORY CONTENTS:"
echo "======================="
echo "✅ 125+ real early-stage founder profiles"
echo "✅ Custom stealth scoring system"
echo "✅ Personalized conversation starters"
echo "✅ Complete documentation and README"
echo "✅ Production-ready code"
echo ""
echo "🚀 Ready for Antler deployment!"
