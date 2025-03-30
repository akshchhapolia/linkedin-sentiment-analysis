import os
import time
import logging
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LinkedInScraper:
    """A class to scrape publicly available LinkedIn posts for a given company."""
    
    def __init__(self):
        """Initialize the LinkedIn scraper with browser settings."""
        self.username = os.getenv('LINKEDIN_USERNAME')
        self.password = os.getenv('LINKEDIN_PASSWORD')
        
        if not self.username or not self.password:
            logger.error("LinkedIn credentials not found in environment variables")
            raise ValueError("LinkedIn credentials not found. Please set LINKEDIN_USERNAME and LINKEDIN_PASSWORD in your .env file")
        
        # Set up Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run in headless mode
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize the WebDriver
        self.driver = None
    
    def __enter__(self):
        """Set up the WebDriver when entering the context."""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the WebDriver when exiting the context."""
        if self.driver:
            self.driver.quit()
    
    def login(self):
        """Log in to LinkedIn."""
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            
            logger.info("Successfully logged in to LinkedIn")
            return True
        
        except Exception as e:
            logger.error(f"Failed to log in to LinkedIn: {str(e)}")
            return False
    
    def search_company(self, company_name: str) -> str:
        """
        Search for a company and return its LinkedIn URL.
        
        Args:
            company_name: Name of the company to search for
            
        Returns:
            The LinkedIn URL of the company
        """
        try:
            search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name.replace(' ', '%20')}"
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search-result__info"))
            )
            
            # Get the first search result
            first_result = self.driver.find_element(By.CSS_SELECTOR, ".search-result__info a")
            company_url = first_result.get_attribute("href")
            
            logger.info(f"Found company URL: {company_url}")
            return company_url
        
        except Exception as e:
            logger.error(f"Failed to search for company: {str(e)}")
            return ""
    
    def get_company_posts(self, company_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get posts from a company's LinkedIn page.
        
        Args:
            company_name: Name of the company
            limit: Maximum number of posts to scrape
            
        Returns:
            A list of dictionaries containing post data
        """
        posts = []
        
        try:
            # Log in to LinkedIn
            if not self.login():
                logger.error("LinkedIn login failed. Cannot proceed.")
                return posts
            
            # Search for the company
            company_url = self.search_company(company_name)
            if not company_url:
                logger.error(f"Could not find LinkedIn page for {company_name}")
                return posts
            
            # Go to the company's posts page
            posts_url = f"{company_url}posts/"
            self.driver.get(posts_url)
            
            # Wait for posts to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-shared-update-v2"))
            )
            
            # Scroll down to load more posts
            for _ in range(min(5, limit // 10)):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Extract posts
            post_elements = self.driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2")
            
            for i, post in enumerate(post_elements[:limit]):
                try:
                    # Extract text content
                    text_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-update-v2__description")
                    text = text_element.text
                    
                    # Extract post date
                    date_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-actor__sub-description")
                    date = date_element.text
                    
                    # Get post URL
                    post_url_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-update-v2__update-link-container a")
                    post_url = post_url_element.get_attribute("href")
                    
                    # Add to posts list
                    posts.append({
                        "company": company_name,
                        "text": text,
                        "date": date,
                        "url": post_url
                    })
                    
                except Exception as e:
                    logger.warning(f"Failed to extract data from post {i + 1}: {str(e)}")
                    continue
            
            logger.info(f"Successfully scraped {len(posts)} posts from {company_name}")
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn posts: {str(e)}")
        
        return posts

# For testing purposes
if __name__ == "__main__":
    with LinkedInScraper() as scraper:
        # Replace with the company name you want to scrape
        company_posts = scraper.get_company_posts("Microsoft")
        
        for post in company_posts:
            print(f"Date: {post['date']}")
            print(f"Text: {post['text'][:100]}...")
            print(f"URL: {post['url']}")
            print("-" * 80) 