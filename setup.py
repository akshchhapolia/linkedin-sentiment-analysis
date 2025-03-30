import os
from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read long description from README
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="social_media_sentiment_analysis",
    version="0.1.0",
    description="A tool to analyze LinkedIn posts and generate sentiment reports with actionable insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI Assisted Developer",
    author_email="example@example.com",
    url="https://github.com/yourusername/social-media-sentiment-analysis",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'sentiment-analysis=src.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 