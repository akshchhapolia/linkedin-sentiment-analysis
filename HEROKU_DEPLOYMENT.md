# Heroku Deployment Guide

This guide will help you deploy the LinkedIn Sentiment Analysis application to Heroku.

## Prerequisites

1. A Heroku account (sign up at [heroku.com](https://signup.heroku.com/) if you don't have one)
2. Git installed on your computer

## Step 1: Prepare Your Application

Your application is already prepared for Heroku with:
- Procfile (specifies the command to run)
- requirements.txt (lists dependencies)
- runtime.txt (specifies Python version)
- Code updates to use environment variables for PORT

## Step 2: Deploy to Heroku

### Using the Heroku Website (No CLI required)

1. Go to [Heroku Dashboard](https://dashboard.heroku.com/)
2. Click "New" → "Create new app"
3. Give your app a name (e.g., linkedin-sentiment-analysis)
4. Choose your region (US or Europe) and click "Create app"
5. In the "Deployment method" section, click on "GitHub"
6. Connect your GitHub account if not already connected
7. Search for your repository "linkedin-sentiment-analysis"
8. Click "Connect" next to your repository
9. Scroll down to "Manual deploy" section
10. Choose the branch (main) and click "Deploy Branch"
11. Wait for the deployment to complete
12. Click "View" to open your application

### Using Git Directly (Alternative)

If you prefer using Git commands directly:

```bash
# Log in to Heroku (you'll be prompted to enter your credentials in a browser)
heroku login

# Create a Heroku app
heroku create linkedin-sentiment-analysis

# Add the Heroku remote to your Git repository
git remote add heroku https://git.heroku.com/linkedin-sentiment-analysis.git

# Push your code to Heroku
git push heroku main
```

## Step 3: Configure Environment Variables (if needed)

If your app requires any environment variables:

1. Go to your app's dashboard on Heroku
2. Click on "Settings"
3. Scroll down to "Config Vars" and click "Reveal Config Vars"
4. Add any required environment variables

## Troubleshooting

If you encounter issues:

1. Check logs: On the Heroku dashboard, go to "More" → "View logs"
2. Ensure all dependencies are in requirements.txt
3. Make sure your app binds to the PORT provided by Heroku
4. Check if your app requires additional buildpacks

## Scaling

By default, your app will use 1 web dyno. You can scale up/down as needed:

1. Go to your app's dashboard on Heroku
2. Click on "Resources"
3. Adjust the slider for web dynos

Note: Free tier has limitations and may sleep after 30 minutes of inactivity. 