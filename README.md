# LinkedIn Sentiment Analysis Tool

**GitHub Repository**: [https://github.com/akshchhapolia/linkedin-sentiment-analysis](https://github.com/akshchhapolia/linkedin-sentiment-analysis)

**Local Demo**: [http://127.0.0.1:5006/](http://127.0.0.1:5006/) (Available when running locally)

A web application that analyzes sentiment from LinkedIn posts for any company, generating comprehensive reports with industry-specific insights.

## Hosting Options

This application can be deployed to various cloud platforms:

1. **Heroku** - Easy deployment with Git integration
   ```bash
   # Install Heroku CLI
   # Login and create app
   heroku login
   heroku create linkedin-sentiment-app
   git push heroku main
   ```

2. **Railway** - Simple deployment with GitHub integration
   - Connect your GitHub repository
   - Set Python as the runtime
   - Add environment variables if needed

3. **Render** - Free tier available for web services
   - Create a new Web Service
   - Connect to your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python linkedin_sentiment_ui.py`

4. **PythonAnywhere** - Specialized Python hosting
   - Upload your files or clone from GitHub
   - Set up a web app with Flask
   - Configure WSGI file to point to your application

## Features

- **Company Analysis**: Analyze sentiment for any company's LinkedIn presence
- **Real-time Scraping**: Attempts to scrape real LinkedIn data (falls back to generated data if needed)
- **Industry-specific Analysis**: Customized insights based on detected company type (fintech, tech, food, travel, retail)
- **Comprehensive Reporting**:
  - Overall sentiment distribution
  - Sentiment trends over time
  - Top positive features and negative issues
  - Sample posts (most positive & negative)
  - Industry-specific priority areas with actionable recommendations

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/linkedin-sentiment-analysis.git
cd linkedin-sentiment-analysis
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application
```bash
python linkedin_sentiment_ui.py
```

2. Open your browser and navigate to http://127.0.0.1:5006/

3. Enter a company name and the number of posts to analyze

4. Click "Generate Sentiment Analysis" to see results

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask (Python)
- **Data Processing**: NLTK for sentiment analysis
- **Web Scraping**: Selenium for LinkedIn data collection

## Structure

- `linkedin_sentiment_ui.py`: Main Flask application
- `linkedin_sentiment_analysis.py`: Core sentiment analysis logic
- `linkedin_scraper.py`: LinkedIn data scraping functionality
- `templates/`: HTML templates for the web interface

## License

MIT

## Disclaimer

This tool is for educational purposes only. Scraping LinkedIn data may violate LinkedIn's terms of service. Always review and comply with LinkedIn's robots.txt and terms of service before deploying in a production environment. 