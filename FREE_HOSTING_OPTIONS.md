# Free Hosting Options for LinkedIn Sentiment Analysis

Since Heroku now requires a credit card, here are some completely free alternatives:

## 1. Render.com
- **Free Tier**: Yes, no credit card required
- **Setup**:
  1. Create account at render.com
  2. Click "New Web Service"
  3. Connect your GitHub repository
  4. Select "Python" as runtime
  5. Set build command: `pip install -r requirements.txt`
  6. Set start command: `gunicorn linkedin_sentiment_ui:app --bind 0.0.0.0:$PORT`
  7. Choose "Free" plan

## 2. PythonAnywhere
- **Free Tier**: Yes, generous free tier
- **Setup**:
  1. Sign up at pythonanywhere.com
  2. Go to the Dashboard
  3. Click on "Web" tab
  4. Create a new web app with Flask
  5. Clone your repository from GitHub
  6. Configure WSGI file to point to your app
  7. Set up virtual environment and install requirements

## 3. Fly.io
- **Free Tier**: Yes (limited resources but enough for this app)
- **Setup**:
  1. Sign up at fly.io (requires credit card but has a free tier)
  2. Install Fly CLI
  3. Run `flyctl auth login`
  4. In your project folder, run `flyctl launch`
  5. Deploy with `flyctl deploy`

## 4. Railway.app
- **Free Tier**: Limited but available
- **Setup**:
  1. Sign up at railway.app
  2. Create new project
  3. Connect GitHub repository
  4. Railway will detect it's a Python app
  5. Add environment variables if needed
  6. Deploy

## 5. GitHub Pages + API
- For a static frontend with API backend:
  1. Host the frontend on GitHub Pages
  2. Use a serverless function provider for the API portion

## Quick Deployment Guide for Render.com

1. Create an account at [Render.com](https://render.com/)
2. Click "New Web Service"
3. Connect to your GitHub repository
4. Configure your service:
   - Name: linkedin-sentiment-analysis
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn linkedin_sentiment_ui:app --bind 0.0.0.0:$PORT`
5. Select Free plan
6. Click "Create Web Service"

Your app will be live in a few minutes at a URL like: `https://linkedin-sentiment-analysis.onrender.com` 