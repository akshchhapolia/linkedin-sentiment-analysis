import sys
import os
import unittest
import tempfile
import shutil

# Add parent directory to path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.report_generation import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    """Unit tests for the ReportGenerator class."""
    
    def setUp(self):
        """Set up the test case."""
        # Create a temporary directory for output
        self.temp_dir = tempfile.mkdtemp()
        self.report_generator = ReportGenerator(output_dir=self.temp_dir)
        
        # Sample data for testing
        self.company_name = "Test Company"
        self.aggregated_results = {
            "sentiment_counts": {"positive": 25, "neutral": 10, "negative": 15},
            "emotion_distribution": {"joy": 0.4, "sadness": 0.2, "anger": 0.1, "fear": 0.1, "surprise": 0.2},
            "average_sentiment": 0.15
        }
        
        self.analyzed_posts = [
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
    
    def tearDown(self):
        """Clean up after the test."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_generate_text_report(self):
        """Test generating a text report."""
        report_path = self.report_generator.generate_text_report(
            self.company_name, 
            self.analyzed_posts, 
            self.aggregated_results
        )
        
        # Check that the report was created
        self.assertTrue(os.path.exists(report_path))
        
        # Check file content
        with open(report_path, "r") as f:
            content = f.read()
            self.assertIn("Sentiment Analysis Report: Test Company", content)
            self.assertIn("Positive posts: 25", content)
            self.assertIn("Actionable Insights", content)
    
    def test_generate_visualization(self):
        """Test generating visualization."""
        viz_path = self.report_generator.generate_visualization(
            self.company_name, 
            self.aggregated_results
        )
        
        # Check that the visualization was created
        self.assertTrue(os.path.exists(viz_path))
    
    def test_save_raw_data(self):
        """Test saving raw data."""
        data_path = self.report_generator.save_raw_data(
            self.company_name, 
            self.analyzed_posts, 
            self.aggregated_results
        )
        
        # Check that the data file was created
        self.assertTrue(os.path.exists(data_path))
    
    def test_generate_report(self):
        """Test generating a complete report."""
        report_files = self.report_generator.generate_report(
            self.company_name, 
            self.analyzed_posts, 
            self.aggregated_results
        )
        
        # Check that all report files were created
        self.assertIn("text_report", report_files)
        self.assertIn("visualization", report_files)
        self.assertIn("raw_data", report_files)
        
        for file_path in report_files.values():
            self.assertTrue(os.path.exists(file_path))

if __name__ == "__main__":
    unittest.main() 