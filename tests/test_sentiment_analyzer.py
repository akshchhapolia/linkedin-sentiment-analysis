import sys
import os
import unittest

# Add parent directory to path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sentiment_analysis import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    """Unit tests for the SentimentAnalyzer class."""
    
    def setUp(self):
        """Set up the test case."""
        self.analyzer = SentimentAnalyzer()
    
    def test_analyze_sentiment_positive(self):
        """Test sentiment analysis with positive text."""
        text = "I love this product! It's amazing and works perfectly."
        result = self.analyzer.analyze_sentiment(text)
        
        self.assertEqual(result["category"], "positive")
        self.assertGreater(result["scores"]["compound"], 0)
    
    def test_analyze_sentiment_negative(self):
        """Test sentiment analysis with negative text."""
        text = "This is terrible. I hate it and will never buy it again."
        result = self.analyzer.analyze_sentiment(text)
        
        self.assertEqual(result["category"], "negative")
        self.assertLess(result["scores"]["compound"], 0)
    
    def test_analyze_sentiment_neutral(self):
        """Test sentiment analysis with neutral text."""
        text = "The product arrived today. It has four components and a manual."
        result = self.analyzer.analyze_sentiment(text)
        
        self.assertEqual(result["category"], "neutral")
    
    def test_analyze_emotion(self):
        """Test emotion analysis."""
        text = "I am so happy with my purchase! It exceeded all my expectations."
        emotions = self.analyzer.analyze_emotion(text)
        
        # Check that joy is one of the emotions detected
        self.assertIn("joy", emotions.keys())
    
    def test_analyze_posts(self):
        """Test analyzing a list of posts."""
        posts = [
            {"text": "I love this company!", "date": "2023-01-01"},
            {"text": "The service was terrible.", "date": "2023-01-02"},
            {"text": "Product arrived on schedule.", "date": "2023-01-03"}
        ]
        
        analyzed_posts = self.analyzer.analyze_posts(posts)
        
        self.assertEqual(len(analyzed_posts), 3)
        self.assertIn("sentiment", analyzed_posts[0])
        self.assertIn("emotions", analyzed_posts[0])
    
    def test_get_aggregated_results(self):
        """Test aggregating analysis results."""
        analyzed_posts = [
            {
                "text": "I love this!",
                "sentiment": {"category": "positive", "scores": {"compound": 0.7}},
                "emotions": {"joy": 0.8, "sadness": 0.1}
            },
            {
                "text": "I hate this!",
                "sentiment": {"category": "negative", "scores": {"compound": -0.7}},
                "emotions": {"anger": 0.8, "joy": 0.1}
            },
            {
                "text": "This is okay.",
                "sentiment": {"category": "neutral", "scores": {"compound": 0.1}},
                "emotions": {"surprise": 0.5, "joy": 0.3}
            }
        ]
        
        results = self.analyzer.get_aggregated_results(analyzed_posts)
        
        self.assertIn("sentiment_counts", results)
        self.assertIn("emotion_distribution", results)
        self.assertIn("average_sentiment", results)
        
        self.assertEqual(results["sentiment_counts"]["positive"], 1)
        self.assertEqual(results["sentiment_counts"]["negative"], 1)
        self.assertEqual(results["sentiment_counts"]["neutral"], 1)
        
        self.assertAlmostEqual(results["average_sentiment"], 0.03333, delta=0.1)

if __name__ == "__main__":
    unittest.main() 