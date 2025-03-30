#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -m nltk.downloader vader_lexicon

echo "Build completed successfully!" 