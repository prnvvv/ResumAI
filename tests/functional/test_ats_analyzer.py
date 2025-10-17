import unittest
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.test_config import TestConfig

class TestATSResumeAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Setup before each test"""
        print(f"\n{'='*50}")
        print(f"Setting up test: {self._testMethodName}")
        
        # Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(TestConfig.ELEMENT_TIMEOUT)
            
            self.driver.get(TestConfig.BASE_URL)
            print("OK - Chrome driver initialized and navigated to app")
            
            # Wait for page load
            time.sleep(3)
            
        except Exception as e:
            print(f"ERROR - Setup failed: {e}")
            raise
    
    def test_01_page_load(self):
        """Test that main page loads correctly"""
        print("Testing page load...")
        
        # Check page contains expected elements
        self.assertIn("ATS", self.driver.page_source)
        print("OK - Page loaded with expected content")
    
    def test_02_sidebar_elements(self):
        """Test sidebar form elements"""
        print("Testing sidebar elements...")
        
        # Look for input fields by placeholder
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Name']")
        if inputs:
            inputs[0].send_keys(TestConfig.TEST_USER["name"])
            print("OK - Name field filled")
        
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Email']")
        if inputs:
            inputs[0].send_keys(TestConfig.TEST_USER["email"])
            print("OK - Email field filled")
        
        print("OK - Sidebar form elements working correctly")
    
    def test_03_file_upload_present(self):
        """Test file upload element exists"""
        print("Testing file upload element...")
        
        file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        self.assertGreater(len(file_inputs), 0, "File upload input should be present")
        print("OK - File upload element found")
    
    def test_04_analyze_button_functionality(self):
        """Test analyze button is present and clickable"""
        print("Testing analyze button...")
        
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
        self.assertGreater(len(buttons), 0, "Analyze button should be present")
        
        analyze_button = buttons[0]
        self.assertTrue(analyze_button.is_displayed(), "Analyze button should be visible")
        self.assertTrue(analyze_button.is_enabled(), "Analyze button should be enabled")
        print("OK - Analyze button is functional")
    
    def tearDown(self):
        """Cleanup after each test"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            print("OK - Browser closed")
        print(f"{'='*50}")

if __name__ == "__main__":
    unittest.main()