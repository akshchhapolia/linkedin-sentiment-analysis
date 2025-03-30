import logging
import nltk
from typing import Dict, List, Any, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {str(e)}")

class SentimentAnalyzer:
    """A class to analyze sentiment and emotions in text."""
    
    def __init__(self):
        """Initialize the sentiment analyzers."""
        # Initialize VADER sentiment analyzer
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize emotion classifier
        try:
            # Using a pre-trained emotion classifier model
            model_name = "j-hartmann/emotion-english-distilroberta-base"
            self.emotion_classifier = pipeline(
                "text-classification", 
                model=model_name, 
                return_all_scores=True
            )
            logger.info("Emotion classifier loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load emotion classifier: {str(e)}")
            self.emotion_classifier = None
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of a text using VADER.
        
        Args:
            text: The text to analyze
            
        Returns:
            A dictionary containing sentiment scores and category
        """
        try:
            # Get VADER sentiment scores
            sentiment_scores = self.vader_analyzer.polarity_scores(text)
            
            # Determine sentiment category
            if sentiment_scores['compound'] >= 0.05:
                sentiment_category = "positive"
            elif sentiment_scores['compound'] <= -0.05:
                sentiment_category = "negative"
            else:
                sentiment_category = "neutral"
            
            return {
                "scores": sentiment_scores,
                "category": sentiment_category
            }
        
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {
                "scores": {"neg": 0, "neu": 0, "pos": 0, "compound": 0},
                "category": "neutral"
            }
    
    def analyze_emotion(self, text: str) -> Dict[str, float]:
        """
        Analyze the emotions in a text.
        
        Args:
            text: The text to analyze
            
        Returns:
            A dictionary mapping emotion labels to scores
        """
        emotions = {}
        
        if not self.emotion_classifier:
            logger.warning("Emotion classifier not available")
            return emotions
        
        try:
            # Truncate text if it's too long for the model
            max_length = 512
            if len(text.split()) > max_length:
                text = ' '.join(text.split()[:max_length])
            
            # Get emotion scores
            emotion_results = self.emotion_classifier(text)[0]
            
            # Convert to dictionary
            for emotion in emotion_results:
                emotions[emotion['label']] = emotion['score']
            
            return emotions
        
        except Exception as e:
            logger.error(f"Error in emotion analysis: {str(e)}")
            return emotions
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform full sentiment and emotion analysis on a text.
        
        Args:
            text: The text to analyze
            
        Returns:
            A dictionary containing sentiment and emotion analysis results
        """
        if not text or text.strip() == "":
            return {
                "sentiment": {
                    "category": "neutral",
                    "scores": {"neg": 0, "neu": 1, "pos": 0, "compound": 0}
                },
                "emotions": {}
            }
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(text)
        
        # Analyze emotions
        emotions = self.analyze_emotion(text)
        
        return {
            "sentiment": sentiment,
            "emotions": emotions
        }
    
    def analyze_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment and emotions for a list of posts.
        
        Args:
            posts: A list of post dictionaries with 'text' keys
            
        Returns:
            The posts with added sentiment and emotion analysis results
        """
        analyzed_posts = []
        
        for post in posts:
            if "text" not in post or not post["text"]:
                continue
            
            # Analyze text
            analysis_results = self.analyze_text(post["text"])
            
            # Add analysis results to post
            post_with_analysis = {**post, **analysis_results}
            analyzed_posts.append(post_with_analysis)
        
        return analyzed_posts
    
    def get_aggregated_results(self, analyzed_posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate sentiment and emotion analysis results.
        
        Args:
            analyzed_posts: A list of posts with sentiment and emotion analysis results
            
        Returns:
            A dictionary with aggregated statistics
        """
        if not analyzed_posts:
            return {
                "sentiment_counts": {"positive": 0, "neutral": 0, "negative": 0},
                "emotion_distribution": {},
                "average_sentiment": 0
            }
        
        # Count sentiment categories
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        compound_scores = []
        
        # Aggregate emotions
        all_emotions = {}
        
        for post in analyzed_posts:
            # Count sentiment categories
            category = post.get("sentiment", {}).get("category", "neutral")
            sentiment_counts[category] = sentiment_counts.get(category, 0) + 1
            
            # Collect compound scores
            compound_score = post.get("sentiment", {}).get("scores", {}).get("compound", 0)
            compound_scores.append(compound_score)
            
            # Aggregate emotions
            for emotion, score in post.get("emotions", {}).items():
                if emotion not in all_emotions:
                    all_emotions[emotion] = []
                all_emotions[emotion].append(score)
        
        # Calculate average compound score
        average_sentiment = sum(compound_scores) / len(compound_scores) if compound_scores else 0
        
        # Calculate average emotion scores
        emotion_distribution = {}
        for emotion, scores in all_emotions.items():
            emotion_distribution[emotion] = sum(scores) / len(scores) if scores else 0
        
        return {
            "sentiment_counts": sentiment_counts,
            "emotion_distribution": emotion_distribution,
            "average_sentiment": average_sentiment
        }

# For testing purposes
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Test with a sample text
    sample_text = "I absolutely love this product! The customer service was excellent."
    result = analyzer.analyze_text(sample_text)
    
    print("Sentiment category:", result["sentiment"]["category"])
    print("Sentiment scores:", result["sentiment"]["scores"])
    print("Emotions:", result["emotions"]) 