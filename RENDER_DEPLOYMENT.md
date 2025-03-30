# Deploying to Render.com

Follow these steps to deploy your LinkedIn Sentiment Analysis tool on Render.com:

## Step 1: Create a Render Account

1. Go to [Render.com](https://render.com/) and sign up for a free account
2. You can sign up with GitHub to make the connection easier

## Step 2: Create a New Web Service

1. After logging in, click the "New +" button in the top right corner
2. Select "Web Service" from the dropdown menu

## Step 3: Connect Your GitHub Repository

1. Choose "GitHub" as your deployment method
2. Connect your GitHub account if prompted
3. Search for and select your repository: `akshchhapolia/linkedin-sentiment-analysis`

## Step 4: Configure Your Web Service

Enter the following configuration settings:

- **Name**: `linkedin-sentiment-analysis` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose the one closest to you
- **Branch**: `main`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn linkedin_sentiment_ui:app --bind 0.0.0.0:$PORT`
- **Plan**: `Free`

## Step 5: Create Web Service

1. Click the "Create Web Service" button
2. Wait for the deployment to complete (this might take 5-10 minutes for the first build)

## Step 6: Access Your Application

1. Once deployment is complete, Render will provide a URL like:
   `https://linkedin-sentiment-analysis.onrender.com`
2. Click on this URL to access your live application

## Troubleshooting

If you encounter any issues:

1. Check the "Logs" tab in your Render dashboard to see what went wrong
2. Common issues:
   - The application needs a specific version of a package
   - NLTK data not downloading correctly
   - Port binding issues

3. If you make changes to fix issues, simply push to your GitHub repository and Render will automatically redeploy

## Additional Notes

- The free plan on Render will automatically "sleep" after 15 minutes of inactivity
- The first request after inactivity may take a few seconds to respond as the service "wakes up"
- You can upgrade to a paid plan if you need more consistent availability 