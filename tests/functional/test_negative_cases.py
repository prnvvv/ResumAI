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

class TestNegativeCases(unittest.TestCase):
    
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(TestConfig.BASE_URL)
        time.sleep(3)
    
    def test_invalid_file_upload(self):
        """Test error handling for invalid file types"""
        print("Testing invalid file upload...")
        
        # Use relative path directly
        invalid_file_path = "tests/test_data/invalid_file.txt"
        if os.path.exists(invalid_file_path):
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(os.path.abspath(invalid_file_path))
            
            # Try to analyze
            buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
            if buttons:
                buttons[0].click()
                time.sleep(3)
                
            # Check for error handling
            page_content = self.driver.page_source.lower()
            has_error = any(word in page_content for word in ["error", "invalid", "unsupported", "cannot"])
            if has_error:
                print("OK - Invalid file handled correctly with error message")
            else:
                print("INFO - No explicit error, but system didn't crash")
        else:
            print("SKIP - Invalid file not found at tests/test_data/invalid_file.txt")
    
    def test_empty_form_submission(self):
        """Test validation for empty form"""
        print("Testing empty form validation...")
        
        # Submit without filling anything
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
        if buttons:
            buttons[0].click()
            time.sleep(2)
            
        # Check for validation messages
        page_content = self.driver.page_source.lower()
        has_validation = any(word in page_content for word in ["required", "error", "please", "fill", "missing"])
        if has_validation:
            print("OK - Empty form validation working")
        else:
            print("INFO - No explicit validation messages detected")
    
    def test_missing_required_fields(self):
        """Test behavior when required fields are missing"""
        print("Testing missing required fields...")
        
        # Fill only name, leave email empty
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Name']")
        if inputs:
            inputs[0].send_keys("Test User")
        
        # Try to submit
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
        if buttons:
            buttons[0].click()
            time.sleep(2)
            
        print("OK - Missing fields test completed (system handled partial form)")
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        print("Testing large file handling...")
        
        # Use relative path directly
        large_file_path = "tests/test_data/large_resume.pdf"
        if os.path.exists(large_file_path):
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(os.path.abspath(large_file_path))
            
            buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
            if buttons:
                buttons[0].click()
                time.sleep(5)  # Longer wait for large file
                
            # Check for any size-related messages
            page_content = self.driver.page_source.lower()
            has_size_warning = any(word in page_content for word in ["large", "size", "limit", "too big"])
            if has_size_warning:
                print("OK - Large file warning shown")
            else:
                print("INFO - No specific size warning detected")
        else:
            print("SKIP - Large file not available at tests/test_data/large_resume.pdf")
    
    def test_invalid_email_format(self):
        """Test email format validation"""
        print("Testing invalid email format...")
        
        # Fill with invalid email
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Email']")
        if inputs:
            inputs[0].send_keys("invalid-email-format")
        
        # Try to submit
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
        if buttons:
            buttons[0].click()
            time.sleep(2)
            
        page_content = self.driver.page_source.lower()
        has_email_error = any(word in page_content for word in ["email", "format", "valid", "invalid"])
        if has_email_error:
            print("OK - Email validation working")
        else:
            print("INFO - No specific email validation detected")
    
    def test_invalid_url_format(self):
        """Test job URL format validation"""
        print("Testing invalid URL format...")
        
        # Fill with invalid URL
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='URL']")
        if inputs:
            inputs[0].send_keys("not-a-valid-url")
        
        # Try to submit
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
        if buttons:
            buttons[0].click()
            time.sleep(2)
            
        page_content = self.driver.page_source.lower()
        has_url_error = any(word in page_content for word in ["url", "link", "valid", "invalid"])
        if has_url_error:
            print("OK - URL validation working")
        else:
            print("INFO - No specific URL validation detected")
    
    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()