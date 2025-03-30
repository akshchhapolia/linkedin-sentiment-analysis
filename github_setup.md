# GitHub Repository Setup Instructions

Follow these steps to host your LinkedIn Sentiment Analysis tool on GitHub:

## Step 1: Create a GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Sign in to your account (or create one if needed)
3. Click the "+" icon in the top right corner and select "New repository"
4. Set the Repository name to: `linkedin-sentiment-analysis`
5. Add a description: "A tool that analyzes sentiment from LinkedIn posts for any company"
6. Choose "Public" visibility
7. **Do not** initialize the repository with README, .gitignore, or license
8. Click "Create repository"

## Step 2: Connect Your Local Repository
After creating the repository, GitHub will show you commands to run. Use the ones for "push an existing repository from the command line":

```bash
# Make sure you're in your project directory
cd /Users/akshatchhapolia/Documents/Cursor_AI_project_1

# Add the remote repository (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/linkedin-sentiment-analysis.git

# Push your code to GitHub
git push -u origin main
```

You'll be prompted to enter your GitHub username and password. For the password, you'll need to use a personal access token:

## Step 3: Create a Personal Access Token (if needed)
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token" (classic)
3. Give it a name like "LinkedIn Sentiment Analysis"
4. Select the "repo" scope
5. Click "Generate token"
6. **Copy the token immediately** - you won't be able to see it again!

Use this token as your password when Git asks for it.

## Step 4: Verify Your Repository
After pushing successfully, visit:
```
https://github.com/YOUR_USERNAME/linkedin-sentiment-analysis
```

You should see all your project files there. 