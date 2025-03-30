#!/usr/bin/env python3
"""
A simple test script to generate mock data and print it.
This script has no external dependencies.
"""

import random
import datetime
from typing import List, Dict, Any

class MockDataProvider:
    """A simplified version of the MockDataProvider for testing."""
    
    def __init__(self):
        """Initialize the mock data provider."""
        # Sample positive phrases
        self.positive_phrases = [
            "Great experience with {company}!",
            "I love {company}'s products. They're amazing!",
            "The customer service at {company} is excellent."
        ]
        
        # Sample negative phrases
        self.negative_phrases = [
            "Disappointed with {company}'s service.",
            "Had a terrible experience with {company} today.",
            "{company}'s product quality has gone downhill."
        ]
        
        # Sample neutral phrases
        self.neutral_phrases = [
            "Just received my order from {company}.",
            "Using {company}'s services for a project.",
            "Attended a webinar by {company} yesterday."
        ]
    
    def generate_random_date(self) -> str:
        """Generate a random recent date."""
        days_ago = random.randint(1, 30)
        date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")
    
    def generate_random_post_url(self, company: str) -> str:
        """Generate a random post URL."""
        post_id = random.randint(1000000, 9999999)
        company_slug = company.lower().replace(" ", "-")
        return f"https://www.linkedin.com/company/{company_slug}/posts/{post_id}"
    
    def generate_mock_posts(self, company_name: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate mock posts for a company."""
        posts = []
        
        # Determine the distribution of sentiment
        # 60% positive, 20% negative, 20% neutral
        positive_count = max(1, int(count * 0.6))
        negative_count = max(1, int(count * 0.2))
        neutral_count = max(1, count - positive_count - negative_count)
        
        # Generate positive posts
        for _ in range(positive_count):
            text = random.choice(self.positive_phrases).format(company=company_name)
            posts.append({
                "company": company_name,
                "text": text,
                "date": self.generate_random_date(),
                "url": self.generate_random_post_url(company_name)
            })
        
        # Generate negative posts
        for _ in range(negative_count):
            text = random.choice(self.negative_phrases).format(company=company_name)
            posts.append({
                "company": company_name,
                "text": text,
                "date": self.generate_random_date(),
                "url": self.generate_random_post_url(company_name)
            })
        
        # Generate neutral posts
        for _ in range(neutral_count):
            text = random.choice(self.neutral_phrases).format(company=company_name)
            posts.append({
                "company": company_name,
                "text": text,
                "date": self.generate_random_date(),
                "url": self.generate_random_post_url(company_name)
            })
        
        # Shuffle posts to mix sentiment
        random.shuffle(posts)
        
        return posts

def main():
    """Generate and print mock data."""
    company_name = "Test Company"
    post_count = 5
    
    print(f"Generating {post_count} mock posts for {company_name}...")
    print()
    
    provider = MockDataProvider()
    posts = provider.generate_mock_posts(company_name, post_count)
    
    for i, post in enumerate(posts, 1):
        print(f"Post {i}:")
        print(f"Date: {post['date']}")
        print(f"Text: {post['text']}")
        print(f"URL: {post['url']}")
        print("-" * 40)
    
    print()
    print(f"Successfully generated {len(posts)} mock posts.")

if __name__ == "__main__":
    main() 