# Social Media Sentiment Analysis Tool - Usage Guide

## Basic Usage

After installing the tool, you can use it in the following ways:

### 1. Analyze LinkedIn Posts for a Company

```bash
python src/main.py --company "Microsoft"
```

This will:
- Attempt to log in to LinkedIn (requires credentials in `.env` file)
- Search for Microsoft's company page
- Collect up to 50 posts
- Analyze sentiment and emotions
- Generate a report

### 2. Use Mock Data (No LinkedIn Required)

```bash
python src/main.py --company "Microsoft" --use-mock-data
```

This will:
- Generate realistic-looking fake posts for Microsoft
- Analyze sentiment and emotions
- Generate a report

### 3. Generate Text-Only Report (No Visualizations)

```bash
python src/main.py --company "Microsoft" --report-type text
```

### 4. Analyze More or Fewer Posts

```bash
python src/main.py --company "Microsoft" --limit 100
```

### 5. Save Reports to a Custom Directory

```bash
python src/main.py --company "Microsoft" --output-dir "my_reports"
```

## Understanding the Output

### Text Report

The text report contains:
- Summary of sentiment statistics (# of positive, negative, neutral posts)
- Emotion breakdown (joy, sadness, anger, etc.)
- Actionable insights based on the analysis
- Sample of most positive and negative posts

Example insights might include:
- "Overall sentiment is strongly positive. Consider highlighting these positive experiences in marketing materials."
- "Users express significant anger. Promptly address user concerns to prevent reputation damage."

### Visualization

If you use the default `full` report type, you'll also get:
- Sentiment distribution chart
- Emotion distribution chart

### Raw Data

All reports also include a JSON file with the complete raw data for further analysis.

## Troubleshooting

### LinkedIn Login Issues

If you encounter issues with LinkedIn login:
1. Check that your credentials are correct in the `.env` file
2. Make sure your LinkedIn account doesn't require two-factor authentication
3. Try using the `--use-mock-data` flag to test the system without LinkedIn

### Browser Issues

The tool uses Chrome with Selenium for web scraping. If you encounter issues:
1. Make sure Chrome is installed on your system
2. Check that the webdriver is compatible with your Chrome version
3. Try using the `--use-mock-data` flag to test without a browser

### Missing Dependencies

If you get import errors:
1. Make sure you've activated the virtual environment
2. Run `pip install -r requirements.txt` to install dependencies
3. Try installing the package in development mode: `pip install -e .` 