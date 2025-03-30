import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collection import LinkedInScraper

class TestLinkedInScraper(unittest.TestCase):
    """Unit tests for the LinkedInScraper class."""
    
    @patch.dict(os.environ, {"LINKEDIN_USERNAME": "test@example.com", "LINKEDIN_PASSWORD": "testpassword"})
    def test_init(self):
        """Test initialization with environment variables."""
        scraper = LinkedInScraper()
        self.assertEqual(scraper.username, "test@example.com")
        self.assertEqual(scraper.password, "testpassword")
    
    @patch.dict(os.environ, {"LINKEDIN_USERNAME": "", "LINKEDIN_PASSWORD": ""})
    def test_init_missing_credentials(self):
        """Test initialization with missing credentials."""
        with self.assertRaises(ValueError):
            LinkedInScraper()
    
    @patch('src.data_collection.linkedin_scraper.webdriver.Chrome')
    @patch('src.data_collection.linkedin_scraper.Service')
    @patch('src.data_collection.linkedin_scraper.ChromeDriverManager')
    @patch.dict(os.environ, {"LINKEDIN_USERNAME": "test@example.com", "LINKEDIN_PASSWORD": "testpassword"})
    def test_context_manager(self, mock_driver_manager, mock_service, mock_chrome):
        """Test context manager for WebDriver."""
        # Setup mock
        mock_instance = mock_chrome.return_value
        
        # Use context manager
        with LinkedInScraper() as scraper:
            self.assertIsNotNone(scraper.driver)
        
        # Check that quit was called
        mock_instance.quit.assert_called_once()
    
    @patch('src.data_collection.linkedin_scraper.webdriver')
    @patch('src.data_collection.linkedin_scraper.Service')
    @patch('src.data_collection.linkedin_scraper.ChromeDriverManager')
    @patch('src.data_collection.linkedin_scraper.WebDriverWait')
    @patch.dict(os.environ, {"LINKEDIN_USERNAME": "test@example.com", "LINKEDIN_PASSWORD": "testpassword"})
    def test_login(self, mock_wait, mock_driver_manager, mock_service, mock_webdriver):
        """Test login method."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_webdriver.Chrome.return_value = mock_driver
        mock_driver.find_element.return_value = MagicMock()
        
        # Mock WebDriverWait.until to return an element
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = MagicMock()
        
        # Create scraper and log in
        with LinkedInScraper() as scraper:
            scraper.driver = mock_driver
            result = scraper.login()
        
        # Check that login returned True
        self.assertTrue(result)
        
        # Check that the driver methods were called
        mock_driver.get.assert_called_with("https://www.linkedin.com/login")
    
    @patch('src.data_collection.linkedin_scraper.webdriver')
    @patch('src.data_collection.linkedin_scraper.Service')
    @patch('src.data_collection.linkedin_scraper.ChromeDriverManager')
    @patch.dict(os.environ, {"LINKEDIN_USERNAME": "test@example.com", "LINKEDIN_PASSWORD": "testpassword"})
    def test_search_company(self, mock_driver_manager, mock_service, mock_webdriver):
        """Test search_company method."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_webdriver.Chrome.return_value = mock_driver
        
        # Mock find_element to return an anchor with href
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "https://www.linkedin.com/company/microsoft/"
        mock_driver.find_element.return_value = mock_element
        
        # Create scraper and search for company
        with LinkedInScraper() as scraper:
            scraper.driver = mock_driver
            url = scraper.search_company("Microsoft")
        
        # Check the URL was returned
        self.assertEqual(url, "https://www.linkedin.com/company/microsoft/")
        
        # Check that the driver methods were called
        mock_driver.get.assert_called_with("https://www.linkedin.com/search/results/companies/?keywords=Microsoft")
    
    @patch.object(LinkedInScraper, 'login', return_value=True)
    @patch.object(LinkedInScraper, 'search_company', return_value="https://www.linkedin.com/company/microsoft/")
    @patch('src.data_collection.linkedin_scraper.webdriver')
    @patch('src.data_collection.linkedin_scraper.Service')
    @patch('src.data_collection.linkedin_scraper.ChromeDriverManager')
    @patch.dict(os.environ, {"LINKEDIN_USERNAME": "test@example.com", "LINKEDIN_PASSWORD": "testpassword"})
    def test_get_company_posts(self, mock_driver_manager, mock_service, mock_webdriver, 
                               mock_search_company, mock_login):
        """Test get_company_posts method."""
        # Setup mocks
        mock_driver = MagicMock()
        mock_webdriver.Chrome.return_value = mock_driver
        
        # Mock post elements
        mock_post1 = MagicMock()
        mock_post2 = MagicMock()
        mock_driver.find_elements.return_value = [mock_post1, mock_post2]
        
        # Mock post components
        mock_text_element = MagicMock()
        mock_text_element.text = "Sample post text"
        mock_post1.find_element.return_value = mock_text_element
        
        mock_date_element = MagicMock()
        mock_date_element.text = "2 days ago"
        mock_post1.find_element.return_value = mock_date_element
        
        mock_url_element = MagicMock()
        mock_url_element.get_attribute.return_value = "https://www.linkedin.com/posts/1234"
        mock_post1.find_element.return_value = mock_url_element
        
        # Create scraper and get posts
        with LinkedInScraper() as scraper:
            scraper.driver = mock_driver
            posts = scraper.get_company_posts("Microsoft", limit=2)
        
        # Check search_company and login were called
        mock_login.assert_called_once()
        mock_search_company.assert_called_once_with("Microsoft")
        
        # Check that driver.get was called with the posts URL
        mock_driver.get.assert_called_with("https://www.linkedin.com/company/microsoft/posts/")

if __name__ == "__main__":
    unittest.main() 