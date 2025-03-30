import random
import datetime
from typing import List, Dict, Any

class MockDataProvider:
    """A class to provide mock data for testing or when LinkedIn scraping fails."""
    
    def __init__(self):
        """Initialize the mock data provider."""
        # Sample positive phrases
        self.positive_phrases = [
            "Great experience with {company}!",
            "I love {company}'s products. They're amazing!",
            "The customer service at {company} is excellent.",
            "Just had a fantastic interaction with {company}.",
            "{company} has exceeded my expectations again.",
            "Kudos to the team at {company} for their outstanding work.",
            "I'm impressed with the quality of {company}'s solutions.",
            "A big thank you to {company} for their support.",
            "Highly recommend {company} for their professional service.",
            "The new features from {company} are game-changing."
        ]
        
        # Sample negative phrases
        self.negative_phrases = [
            "Disappointed with {company}'s service.",
            "Had a terrible experience with {company} today.",
            "{company}'s product quality has gone downhill.",
            "Customer support at {company} was unhelpful.",
            "Will think twice before using {company} again.",
            "Not satisfied with my recent purchase from {company}.",
            "{company} failed to address my concerns.",
            "The wait time for {company}'s support is unacceptable.",
            "Expected better from {company}.",
            "Frustrated with {company}'s policies."
        ]
        
        # Sample neutral phrases
        self.neutral_phrases = [
            "Just received my order from {company}.",
            "Using {company}'s services for a project.",
            "Attended a webinar by {company} yesterday.",
            "{company} announced new updates today.",
            "Looking for more information about {company}.",
            "Comparing {company} with their competitors.",
            "Noticed {company} has changed their logo.",
            "Saw {company}'s advertisement on my way to work.",
            "{company} is hosting an event next month.",
            "Checking out {company}'s new office location."
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
    
    def generate_mock_posts(self, company_name: str, count: int = 50) -> List[Dict[str, Any]]:
        """
        Generate mock posts for a company.
        
        Args:
            company_name: Name of the company
            count: Number of posts to generate
            
        Returns:
            A list of post dictionaries
        """
        posts = []
        
        # Determine the distribution of sentiment
        # 60% positive, 20% negative, 20% neutral
        positive_count = int(count * 0.6)
        negative_count = int(count * 0.2)
        neutral_count = count - positive_count - negative_count
        
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

# For testing purposes
if __name__ == "__main__":
    provider = MockDataProvider()
    mock_posts = provider.generate_mock_posts("Example Corp", 10)
    
    for post in mock_posts:
        print(f"Date: {post['date']}")
        print(f"Text: {post['text']}")
        print(f"URL: {post['url']}")
        print("-" * 80) 