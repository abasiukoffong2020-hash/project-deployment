#!/bin/bash
# Deploy helper for GitHub + Streamlit Cloud
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh <github-repo-url>

set -e

REPO_URL="$1"
if [ -z "$REPO_URL" ]; then
  echo "Usage: ./deploy.sh <github-repo-url>"
  exit 1
fi

# Install dependencies if needed
python -m pip install -r requirements.txt

# Add files to git, commit, and push
if [ ! -d .git ]; then
  git init
  git branch -M main
fi

git add .
git commit -m "Deploy Streamlit app" || true
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL" || true
git push -u origin main --force

echo "Repo pushed to $REPO_URL"
echo "Now connect the app on Streamlit Cloud: https://share.streamlit.io/"
