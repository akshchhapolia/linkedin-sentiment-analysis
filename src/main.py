import os
import sys
import argparse
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import components
from data_collection import LinkedInScraper, MockDataProvider
from sentiment_analysis import SentimentAnalyzer
from report_generation import ReportGenerator

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Social Media Sentiment Analysis Tool')
    
    parser.add_argument('--company', required=True, help='Name of the company to analyze')
    parser.add_argument('--limit', type=int, default=50, help='Maximum number of posts to analyze')
    parser.add_argument('--report-type', choices=['text', 'full'], default='full', 
                       help='Type of report to generate (text-only or full with visualizations)')
    parser.add_argument('--output-dir', default='reports', help='Directory to save reports')
    parser.add_argument('--use-mock-data', action='store_true', 
                       help='Use mock data instead of scraping LinkedIn')
    
    return parser.parse_args()

def collect_data(company_name: str, limit: int, use_mock_data: bool = False) -> List[Dict[str, Any]]:
    """
    Collect data either by scraping LinkedIn or using mock data.
    
    Args:
        company_name: Name of the company
        limit: Maximum number of posts to collect
        use_mock_data: Whether to use mock data
        
    Returns:
        A list of post dictionaries
    """
    if use_mock_data:
        logger.info(f"Using mock data for {company_name}")
        mock_provider = MockDataProvider()
        return mock_provider.generate_mock_posts(company_name, limit)
    
    # Try to collect data from LinkedIn
    try:
        # Check if LinkedIn credentials are set
        if not os.getenv('LINKEDIN_USERNAME') or not os.getenv('LINKEDIN_PASSWORD'):
            logger.warning("LinkedIn credentials not found. Falling back to mock data.")
            mock_provider = MockDataProvider()
            return mock_provider.generate_mock_posts(company_name, limit)
        
        logger.info(f"Collecting posts from LinkedIn for {company_name}...")
        with LinkedInScraper() as scraper:
            posts = scraper.get_company_posts(company_name, limit=limit)
        
        # If no posts were found, use mock data
        if not posts:
            logger.warning(f"No posts found for {company_name} on LinkedIn. Falling back to mock data.")
            mock_provider = MockDataProvider()
            return mock_provider.generate_mock_posts(company_name, limit)
        
        logger.info(f"Collected {len(posts)} posts from LinkedIn")
        return posts
    
    except Exception as e:
        logger.error(f"Error scraping LinkedIn: {str(e)}. Falling back to mock data.")
        mock_provider = MockDataProvider()
        return mock_provider.generate_mock_posts(company_name, limit)

def main():
    """Main function to run the sentiment analysis tool."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Step 1: Collect data
        posts = collect_data(args.company, args.limit, args.use_mock_data)
        
        if not posts:
            logger.error("No posts collected. Cannot proceed.")
            sys.exit(1)
        
        # Step 2: Analyze sentiment
        logger.info("Analyzing sentiment and emotions...")
        analyzer = SentimentAnalyzer()
        analyzed_posts = analyzer.analyze_posts(posts)
        
        # Step 3: Aggregate results
        aggregated_results = analyzer.get_aggregated_results(analyzed_posts)
        
        # Step 4: Generate report
        logger.info("Generating report...")
        report_generator = ReportGenerator(output_dir=args.output_dir)
        include_viz = args.report_type == 'full'
        report_files = report_generator.generate_report(
            args.company, 
            analyzed_posts, 
            aggregated_results, 
            include_viz=include_viz
        )
        
        # Step 5: Print report locations
        logger.info("Analysis complete!")
        for report_type, file_path in report_files.items():
            logger.info(f"{report_type.replace('_', ' ').title()}: {file_path}")
        
        # Return the path to the text report
        if "text_report" in report_files:
            return report_files["text_report"]
        
    except Exception as e:
        logger.error(f"Error running sentiment analysis tool: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 