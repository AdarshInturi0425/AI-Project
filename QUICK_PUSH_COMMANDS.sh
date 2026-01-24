#!/bin/bash

# Quick reference for pushing changes to Git

echo "=========================================="
echo "Git Push - Quick Reference"
echo "=========================================="

# Option 1: Push to feature branch (RECOMMENDED for collaboration)
echo -e "\n✓ Option 1: Push to Feature Branch (Safe)"
echo "  git add ."
echo "  git commit -m '[DOCS] Add comprehensive documentation'"
echo "  git push origin feature/semantic-layer-pyspark-sql-tests"
echo "  → Then create Pull Request on GitHub"

# Option 2: Push to master (only if you're solo)
echo -e "\n✓ Option 2: Push to Master (Solo only)"
echo "  git checkout master"
echo "  git pull origin master"
echo "  git add ."
echo "  git commit -m '[DOCS] Add comprehensive documentation'"
echo "  git push origin master"

# Verify
echo -e "\n✓ Verify your push:"
echo "  git log --oneline -5"
echo "  git show --name-status"

echo -e "\n=========================================="
echo "Choose Option 1 for team projects"
echo "Choose Option 2 only if working solo"
echo "=========================================="
