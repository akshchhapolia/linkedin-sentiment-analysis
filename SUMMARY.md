# Social Media Sentiment Analysis Tool - System Overview

## Project Summary

This tool analyzes publicly available LinkedIn posts for a company, extracts sentiment and emotions using advanced natural language processing models, and generates reports with actionable insights. The system can be used with real LinkedIn data or mock data for testing purposes.

## Components

### 1. Data Collection Module

The data collection module provides two ways to gather company posts:

- **LinkedIn Scraper**: Automates browsing LinkedIn with Selenium to collect public company posts.
- **Mock Data Provider**: Generates realistic test data with a predefined sentiment distribution.

### 2. Sentiment Analysis Module

The sentiment analysis module analyzes the text content of posts using:

- **VADER Sentiment Analyzer**: A lexicon and rule-based sentiment analysis tool specifically tuned for social media content.
- **Emotion Classifier**: A transformer-based model (RoBERTa) trained to detect emotions like joy, sadness, anger, fear, and surprise.

### 3. Report Generation Module

The report generation module produces three types of outputs:

- **Text Reports**: Detailed analysis with sentiment statistics and actionable insights.
- **Visualizations**: Charts showing sentiment and emotion distribution.
- **Raw Data**: JSON files with complete analysis data for further processing.

## Key Features

- **Flexible Data Source**: Works with LinkedIn data or mock data for testing.
- **Robust Sentiment Analysis**: Combines rule-based and transformer-based models.
- **Actionable Insights**: AI-generated recommendations based on sentiment patterns.
- **Customizable Reports**: Options for text-only or visual reports.
- **Easy Installation**: Automated setup scripts for different platforms.

## Technical Implementation

- **Language**: Python 3.7+
- **Web Scraping**: Selenium with Chrome WebDriver
- **NLP Models**: VADER and RoBERTa-based emotion classifier
- **Visualization**: Matplotlib
- **Packaging**: Standard Python packaging with setuptools

## Security and Privacy

The tool only analyzes publicly available information from company pages on LinkedIn. User credentials for LinkedIn are stored locally in a `.env` file and are not transmitted beyond the necessary login process.

## Testing

The system includes unit tests for each major component:

- Tests for data collection (with mock browser interactions)
- Tests for sentiment analysis (with predefined text examples)
- Tests for report generation (with sample analysis data)

## Future Extensions

The system is designed to be extendable in several ways:

- Additional data sources (Twitter, App Store reviews)
- Scheduled analysis and reporting
- Dashboard integrations
- Additional sentiment models and metrics

## Usage

See the `USAGE.md` file for detailed instructions on how to use the tool, including command-line options and example commands. 