"""
LinkedIn scraper for company posts and user sentiment.
"""

import os
import time
import random
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Set up and return a configured Chrome WebDriver."""
    options = Options()
    
    # For headless operation (no visible browser window)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Set window size to mimic a realistic browser window
    options.add_argument("--window-size=1920,1080")
    
    # Add common user agent
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Prevent detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Create the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute JavaScript to mask Selenium usage
    driver.execute_script("""
    Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
    });
    """)
    
    return driver

def login_to_linkedin(driver, username, password):
    """Log in to LinkedIn with provided credentials."""
    if not username or not password:
        logging.error("LinkedIn credentials not provided")
        return False
    
    # Navigate to LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2, 4))
    
    try:
        # Enter username
        driver.find_element(By.ID, "username").send_keys(username)
        time.sleep(random.uniform(1, 2))
        
        # Enter password
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(random.uniform(1, 2))
        
        # Click login button
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for successful login
        time.sleep(random.uniform(3, 5))
        
        # Check if login was successful
        if "feed" in driver.current_url or "mynetwork" in driver.current_url:
            logging.info("Successfully logged in to LinkedIn")
            return True
        else:
            logging.error("Login failed or security checkpoint encountered")
            return False
    
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return False

def search_company(driver, company_name):
    """Search for a company on LinkedIn and return its URL."""
    try:
        # Navigate to LinkedIn search
        search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name.replace(' ', '%20')}"
        driver.get(search_url)
        time.sleep(random.uniform(3, 5))
        
        # Find the first company result
        company_elements = driver.find_elements(By.CSS_SELECTOR, ".entity-result__title a")
        
        if not company_elements:
            logging.warning(f"No results found for company: {company_name}")
            return None
        
        # Get the URL of the first result
        company_url = company_elements[0].get_attribute("href")
        
        if "linkedin.com/company/" in company_url:
            return company_url
        else:
            return None
            
    except Exception as e:
        logging.error(f"Error searching for company: {str(e)}")
        return None

def get_company_posts(driver, company_url, limit=5):
    """Get posts from a company's LinkedIn page."""
    if not company_url:
        return []
    
    posts = []
    
    try:
        # Navigate to company page
        driver.get(company_url)
        time.sleep(random.uniform(3, 5))
        
        # Check if there's a Posts tab and click it
        try:
            posts_tab = driver.find_element(By.XPATH, "//a[contains(@href, '/posts/')]")
            posts_tab.click()
            time.sleep(random.uniform(2, 4))
        except NoSuchElementException:
            logging.warning("Could not find Posts tab, using default page")
        
        # Scroll a few times to load more posts
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))
        
        # Find all posts
        post_elements = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2")
        
        for post_element in post_elements[:limit]:
            try:
                # Extract text content
                try:
                    text_element = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-update-v2__description")
                    text = text_element.text
                except:
                    try:
                        text_element = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-text")
                        text = text_element.text
                    except:
                        text = "No text available"
                
                # Extract date
                try:
                    date_element = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-actor__sub-description")
                    date_text = date_element.text
                    # Convert LinkedIn's relative dates to actual dates
                    date = convert_linkedin_date(date_text)
                except:
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                # Extract post URL
                try:
                    # First look for a "Copy link to post" button
                    menu_button = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-control-menu__trigger")
                    menu_button.click()
                    time.sleep(0.5)
                    
                    copy_link = driver.find_element(By.XPATH, "//div[text()='Copy link to post']")
                    
                    # Get the URL from the data-clipboard-text attribute
                    url_element = copy_link.find_element(By.XPATH, "./ancestor::li")
                    url = url_element.get_attribute("data-clipboard-text")
                    
                    # Close the menu
                    driver.find_element(By.TAG_NAME, "body").click()
                except:
                    # If we can't get the URL, construct a placeholder
                    url = f"{company_url}/posts/"
                
                # Add to posts list
                posts.append({
                    "text": text,
                    "date": date,
                    "author": company_name,
                    "url": url
                })
                
            except Exception as e:
                logging.warning(f"Error extracting post: {str(e)}")
        
        return posts
        
    except Exception as e:
        logging.error(f"Error getting company posts: {str(e)}")
        return []

def scrape_public_posts(driver, company_name, limit=10):
    """Find and scrape posts from LinkedIn users mentioning the company."""
    posts = []
    
    try:
        # Search for posts mentioning the company
        search_url = f"https://www.linkedin.com/search/results/content/?keywords={company_name.replace(' ', '%20')}"
        driver.get(search_url)
        time.sleep(random.uniform(3, 5))
        
        # Scroll a few times to load more posts
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))
        
        # Find all post elements
        post_elements = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2, .occurrence-search__occurance")
        
        for post_element in post_elements[:limit]:
            try:
                # Extract text content
                try:
                    text_element = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-text")
                    text = text_element.text
                except:
                    try:
                        text_element = post_element.find_element(By.CSS_SELECTOR, ".search-content-entity-lockup__summary")
                        text = text_element.text
                    except:
                        text = "No text available"
                
                # Skip if text doesn't mention the company
                if company_name.lower() not in text.lower():
                    continue
                
                # Extract author
                try:
                    author_element = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-actor__name, .search-content-entity-lockup__entity-info")
                    author = author_element.text
                except:
                    author = "Unknown Author"
                
                # Extract date
                try:
                    date_element = post_element.find_element(By.CSS_SELECTOR, ".feed-shared-actor__sub-description, .search-content-entity-lockup__timestamp")
                    date_text = date_element.text
                    # Convert LinkedIn's relative dates to actual dates
                    date = convert_linkedin_date(date_text)
                except:
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                # Extract post URL
                try:
                    link_element = post_element.find_element(By.CSS_SELECTOR, "a.app-aware-link")
                    url = link_element.get_attribute("href")
                except:
                    url = f"https://www.linkedin.com/search/results/content/?keywords={company_name.replace(' ', '%20')}"
                
                # Add to posts list
                posts.append({
                    "text": text,
                    "date": date,
                    "author": author,
                    "url": url
                })
                
            except Exception as e:
                logging.warning(f"Error extracting public post: {str(e)}")
        
        logging.info(f"Extracted {len(posts)} public posts mentioning the company")
        return posts
        
    except Exception as e:
        logging.error(f"Error getting public posts: {str(e)}")
        return []

def convert_linkedin_date(date_text):
    """Convert LinkedIn's relative date to an actual date string."""
    today = datetime.datetime.now()
    
    if "minute" in date_text or "hour" in date_text:
        return today.strftime("%Y-%m-%d")
    
    if "day" in date_text or "yesterday" in date_text:
        days = 1 if "yesterday" in date_text else int(''.join(filter(str.isdigit, date_text)))
        date = today - datetime.timedelta(days=days)
        return date.strftime("%Y-%m-%d")
    
    if "week" in date_text:
        weeks = int(''.join(filter(str.isdigit, date_text)))
        date = today - datetime.timedelta(weeks=weeks)
        return date.strftime("%Y-%m-%d")
    
    if "month" in date_text:
        months = int(''.join(filter(str.isdigit, date_text)))
        date = today - datetime.timedelta(days=30*months)  # Approximate
        return date.strftime("%Y-%m-%d")
    
    # Handle specific dates like "Jan 5, 2023"
    try:
        date_obj = datetime.datetime.strptime(date_text, "%b %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except:
        return today.strftime("%Y-%m-%d")

def scrape_linkedin_for_company(company_name, post_limit=10, use_mock_data=False):
    """Main function to scrape LinkedIn posts for a specific company."""
    if use_mock_data:
        # Import and use the mock data generator
        from linkedin_sentiment_analysis import generate_company_reviews
        posts = generate_company_reviews(company_name, post_limit)
        return posts, True
    
    posts = []
    driver = None
    
    try:
        driver = setup_driver()
        
        # Log in to LinkedIn
        username = os.environ.get('LINKEDIN_USERNAME')
        password = os.environ.get('LINKEDIN_PASSWORD')
        
        login_successful = login_to_linkedin(driver, username, password)
        
        if not login_successful:
            logging.warning("Login failed, falling back to mock data")
            from linkedin_sentiment_analysis import generate_company_reviews
            posts = generate_company_reviews(company_name, post_limit)
            return posts, False
        
        # Find the company page
        company_url = search_company(driver, company_name)
        
        # Get posts from the company page
        company_posts = get_company_posts(driver, company_url, limit=post_limit//2)
        posts.extend(company_posts)
        
        # Get public posts mentioning the company
        if len(posts) < post_limit:
            public_posts = scrape_public_posts(driver, company_name, limit=post_limit-len(posts))
            posts.extend(public_posts)
        
        logging.info(f"Successfully scraped {len(posts)} LinkedIn posts for {company_name}")
        
        # If we didn't get enough posts, supplement with mock data
        if len(posts) < post_limit:
            logging.info(f"Only found {len(posts)} posts, supplementing with mock data")
            from linkedin_sentiment_analysis import generate_company_reviews
            additional_posts = generate_company_reviews(company_name, post_limit - len(posts))
            posts.extend(additional_posts)
            return posts, False
        
        return posts, True
        
    except Exception as e:
        logging.error(f"Error in LinkedIn scraping: {str(e)}")
        # Fall back to mock data
        logging.warning("Error occurred, falling back to mock data")
        from linkedin_sentiment_analysis import generate_company_reviews
        posts = generate_company_reviews(company_name, post_limit)
        return posts, False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Example usage
    import sys
    
    company = "Microsoft" if len(sys.argv) < 2 else sys.argv[1]
    limit = 10 if len(sys.argv) < 3 else int(sys.argv[2])
    
    posts, real_data = scrape_linkedin_for_company(company, limit)
    
    print(f"{'Real' if real_data else 'Mock'} data for {company}:")
    for i, post in enumerate(posts, 1):
        print(f"\n--- Post {i} ---")
        print(f"Author: {post.get('author', 'Unknown')}")
        print(f"Date: {post.get('date', 'Unknown')}")
        print(f"Text: {post.get('text', 'No text')[:100]}...") 