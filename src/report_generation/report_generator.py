import os
import logging
import json
import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """A class to generate reports based on sentiment analysis results."""
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize the report generator.
        
        Args:
            output_dir: Directory to save the reports
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def _generate_insights(self, aggregated_results: Dict[str, Any]) -> List[str]:
        """
        Generate actionable insights based on sentiment analysis results.
        
        Args:
            aggregated_results: Aggregated sentiment and emotion analysis results
            
        Returns:
            A list of actionable insights
        """
        insights = []
        
        # Extract data
        sentiment_counts = aggregated_results.get("sentiment_counts", {})
        emotion_distribution = aggregated_results.get("emotion_distribution", {})
        average_sentiment = aggregated_results.get("average_sentiment", 0)
        
        # Generate insights based on sentiment
        total_posts = sum(sentiment_counts.values())
        positive_ratio = sentiment_counts.get("positive", 0) / total_posts if total_posts > 0 else 0
        negative_ratio = sentiment_counts.get("negative", 0) / total_posts if total_posts > 0 else 0
        
        # Overall sentiment insights
        if average_sentiment >= 0.25:
            insights.append("Overall sentiment is strongly positive. Consider highlighting these positive experiences in marketing materials.")
        elif average_sentiment >= 0.05:
            insights.append("Sentiment is generally positive. Continue current engagement strategies.")
        elif average_sentiment <= -0.25:
            insights.append("Overall sentiment is strongly negative. Urgent attention is needed to address customer concerns.")
        elif average_sentiment <= -0.05:
            insights.append("Sentiment trends negative. Review recent changes to identify potential issues.")
        else:
            insights.append("Sentiment is mostly neutral. Consider strategies to increase engagement and emotional connection.")
        
        # Emotion-based insights
        if emotion_distribution:
            # Find the dominant emotion
            dominant_emotion = max(emotion_distribution.items(), key=lambda x: x[1])
            
            if dominant_emotion[0] == "joy" and dominant_emotion[1] > 0.3:
                insights.append("Users express significant joy. Leverage this positive emotion in future communications.")
            elif dominant_emotion[0] == "anger" and dominant_emotion[1] > 0.3:
                insights.append("Significant anger detected. Promptly address user concerns to prevent reputation damage.")
            elif dominant_emotion[0] == "sadness" and dominant_emotion[1] > 0.3:
                insights.append("Users express sadness. Consider empathetic communication strategies.")
            elif dominant_emotion[0] == "fear" and dominant_emotion[1] > 0.3:
                insights.append("Users express fear or anxiety. Address concerns with reassuring communications.")
            elif dominant_emotion[0] == "surprise" and dominant_emotion[1] > 0.3:
                insights.append("High surprise indicates unexpected experiences. Review recent changes or announcements.")
        
        # Balance of sentiment
        if positive_ratio > 0.7:
            insights.append("Strong positive sentiment dominates. Capitalize on this goodwill for new initiatives.")
        elif negative_ratio > 0.7:
            insights.append("Strong negative sentiment dominates. Immediate action required to address issues.")
        elif negative_ratio > 0.4 and positive_ratio > 0.4:
            insights.append("Mixed sentiment detected. Further investigation needed to understand diverging user experiences.")
        
        return insights
    
    def generate_text_report(self, company_name: str, analyzed_posts: List[Dict[str, Any]], aggregated_results: Dict[str, Any]) -> str:
        """
        Generate a text-based report from sentiment analysis results.
        
        Args:
            company_name: Name of the company
            analyzed_posts: List of posts with sentiment analysis results
            aggregated_results: Aggregated sentiment and emotion analysis results
            
        Returns:
            Path to the generated report file
        """
        try:
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{company_name.replace(' ', '_')}_{timestamp}_report.txt"
            file_path = os.path.join(self.output_dir, filename)
            
            # Generate actionable insights
            insights = self._generate_insights(aggregated_results)
            
            # Extract data for the report
            sentiment_counts = aggregated_results.get("sentiment_counts", {})
            emotion_distribution = aggregated_results.get("emotion_distribution", {})
            total_posts = sum(sentiment_counts.values())
            
            with open(file_path, "w") as f:
                # Write report header
                f.write(f"# Sentiment Analysis Report: {company_name}\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Write summary statistics
                f.write("## Summary\n\n")
                f.write(f"Total posts analyzed: {total_posts}\n")
                f.write(f"Positive posts: {sentiment_counts.get('positive', 0)} ({(sentiment_counts.get('positive', 0) / total_posts * 100):.1f}%)\n")
                f.write(f"Neutral posts: {sentiment_counts.get('neutral', 0)} ({(sentiment_counts.get('neutral', 0) / total_posts * 100):.1f}%)\n")
                f.write(f"Negative posts: {sentiment_counts.get('negative', 0)} ({(sentiment_counts.get('negative', 0) / total_posts * 100):.1f}%)\n\n")
                
                # Write emotion breakdown
                f.write("## Emotion Analysis\n\n")
                for emotion, score in sorted(emotion_distribution.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{emotion.capitalize()}: {score:.1%}\n")
                f.write("\n")
                
                # Write actionable insights
                f.write("## Actionable Insights\n\n")
                for i, insight in enumerate(insights, 1):
                    f.write(f"{i}. {insight}\n")
                f.write("\n")
                
                # Write sample posts (top positive and negative)
                f.write("## Sample Posts\n\n")
                
                # Sort posts by sentiment score
                sorted_posts = sorted(
                    analyzed_posts, 
                    key=lambda x: x.get("sentiment", {}).get("scores", {}).get("compound", 0),
                    reverse=True
                )
                
                # Write top positive posts
                f.write("### Most Positive Posts\n\n")
                for post in sorted_posts[:3]:
                    score = post.get("sentiment", {}).get("scores", {}).get("compound", 0)
                    f.write(f"Score: {score:.2f}\n")
                    f.write(f"Text: {post.get('text', '')[:200]}...\n\n")
                
                # Write top negative posts
                f.write("### Most Negative Posts\n\n")
                for post in sorted_posts[-3:]:
                    score = post.get("sentiment", {}).get("scores", {}).get("compound", 0)
                    f.write(f"Score: {score:.2f}\n")
                    f.write(f"Text: {post.get('text', '')[:200]}...\n\n")
            
            logger.info(f"Generated text report: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Error generating text report: {str(e)}")
            return ""
    
    def generate_visualization(self, company_name: str, aggregated_results: Dict[str, Any]) -> Optional[str]:
        """
        Generate visualizations for sentiment analysis results.
        
        Args:
            company_name: Name of the company
            aggregated_results: Aggregated sentiment and emotion analysis results
            
        Returns:
            Path to the generated visualization file
        """
        try:
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{company_name.replace(' ', '_')}_{timestamp}_viz.png"
            file_path = os.path.join(self.output_dir, filename)
            
            # Extract data
            sentiment_counts = aggregated_results.get("sentiment_counts", {})
            emotion_distribution = aggregated_results.get("emotion_distribution", {})
            
            # Create figure with 2 subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Plot sentiment distribution
            sentiment_labels = list(sentiment_counts.keys())
            sentiment_values = list(sentiment_counts.values())
            ax1.bar(sentiment_labels, sentiment_values, color=['green', 'gray', 'red'])
            ax1.set_title('Sentiment Distribution')
            ax1.set_ylabel('Number of Posts')
            
            # Plot emotion distribution
            emotion_labels = list(emotion_distribution.keys())
            emotion_values = list(emotion_distribution.values())
            
            # Sort emotions by value
            sorted_emotions = sorted(zip(emotion_labels, emotion_values), key=lambda x: x[1], reverse=True)
            emotion_labels = [e[0] for e in sorted_emotions]
            emotion_values = [e[1] for e in sorted_emotions]
            
            ax2.bar(emotion_labels, emotion_values)
            ax2.set_title('Emotion Distribution')
            ax2.set_ylabel('Average Score')
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
            # Add overall title
            plt.suptitle(f"Sentiment Analysis Results: {company_name}")
            
            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()
            
            logger.info(f"Generated visualization: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
            return None
    
    def save_raw_data(self, company_name: str, analyzed_posts: List[Dict[str, Any]], aggregated_results: Dict[str, Any]) -> str:
        """
        Save raw data for further analysis.
        
        Args:
            company_name: Name of the company
            analyzed_posts: List of posts with sentiment analysis results
            aggregated_results: Aggregated sentiment and emotion analysis results
            
        Returns:
            Path to the saved data file
        """
        try:
            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{company_name.replace(' ', '_')}_{timestamp}_data.json"
            file_path = os.path.join(self.output_dir, filename)
            
            # Prepare data for serialization
            data = {
                "company": company_name,
                "timestamp": datetime.datetime.now().isoformat(),
                "aggregated_results": aggregated_results,
                "posts": analyzed_posts
            }
            
            # Save to file
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved raw data: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Error saving raw data: {str(e)}")
            return ""
    
    def generate_report(self, company_name: str, analyzed_posts: List[Dict[str, Any]], aggregated_results: Dict[str, Any], include_viz: bool = True) -> Dict[str, str]:
        """
        Generate a complete report including text, visualizations, and raw data.
        
        Args:
            company_name: Name of the company
            analyzed_posts: List of posts with sentiment analysis results
            aggregated_results: Aggregated sentiment and emotion analysis results
            include_viz: Whether to include visualizations
            
        Returns:
            A dictionary with paths to the generated files
        """
        report_files = {}
        
        # Generate text report
        text_report_path = self.generate_text_report(company_name, analyzed_posts, aggregated_results)
        if text_report_path:
            report_files["text_report"] = text_report_path
        
        # Generate visualization if requested
        if include_viz:
            viz_path = self.generate_visualization(company_name, aggregated_results)
            if viz_path:
                report_files["visualization"] = viz_path
        
        # Save raw data
        data_path = self.save_raw_data(company_name, analyzed_posts, aggregated_results)
        if data_path:
            report_files["raw_data"] = data_path
        
        return report_files

# For testing purposes
if __name__ == "__main__":
    # Sample data
    aggregated_results = {
        "sentiment_counts": {"positive": 25, "neutral": 10, "negative": 15},
        "emotion_distribution": {"joy": 0.4, "sadness": 0.2, "anger": 0.1, "fear": 0.1, "surprise": 0.2},
        "average_sentiment": 0.15
    }
    
    analyzed_posts = [
        {
            "text": "I love this company's products! They're amazing.",
            "sentiment": {"category": "positive", "scores": {"neg": 0.0, "neu": 0.3, "pos": 0.7, "compound": 0.8}},
            "emotions": {"joy": 0.8, "sadness": 0.05, "anger": 0.05, "fear": 0.05, "surprise": 0.05}
        },
        {
            "text": "The customer service is terrible. I'll never buy from them again.",
            "sentiment": {"category": "negative", "scores": {"neg": 0.7, "neu": 0.3, "pos": 0.0, "compound": -0.8}},
            "emotions": {"joy": 0.05, "sadness": 0.2, "anger": 0.6, "fear": 0.1, "surprise": 0.05}
        }
    ]
    
    # Generate report
    report_generator = ReportGenerator()
    reports = report_generator.generate_report("Test Company", analyzed_posts, aggregated_results)
    
    print("Generated files:")
    for report_type, file_path in reports.items():
        print(f"{report_type}: {file_path}") 