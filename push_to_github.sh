#!/bin/bash

echo "🚀 Pushing founder_antler to GitHub..."
echo ""

# Check if remote is already configured
if git remote -v | grep -q "origin"; then
    echo "✅ Remote origin already configured"
    echo "Pushing to GitHub..."
    git push -u origin main
else
    echo "❌ No remote origin configured"
    echo ""
    echo "📋 Please follow these steps:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: founder_antler"
    echo "3. Description: Founder Sourcing & Scoring System for Antler"
    echo "4. Make it Public or Private"
    echo "5. DO NOT initialize with README"
    echo "6. Click 'Create repository'"
    echo ""
    echo "7. Then run these commands:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/founder_antler.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "Replace YOUR_USERNAME with your actual GitHub username"
fi
