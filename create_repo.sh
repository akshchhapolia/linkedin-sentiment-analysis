#!/bin/bash

# Replace with your GitHub username
USERNAME="akshatchhapolia"

# Prompt for personal access token
echo "Enter your GitHub Personal Access Token:"
read -s TOKEN

# Repository details
REPO_NAME="linkedin-sentiment-analysis"
REPO_DESC="A tool that analyzes sentiment from LinkedIn posts for any company"
REPO_VISIBILITY="public"

# Create repository
curl -X POST \
  -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"${REPO_NAME}\",\"description\":\"${REPO_DESC}\",\"private\":false}"

echo "Repository created: https://github.com/${USERNAME}/${REPO_NAME}"

# Set the remote URL
git remote add origin https://github.com/${USERNAME}/${REPO_NAME}.git

echo "Remote origin added. Run 'git push -u origin main' to push your code." 