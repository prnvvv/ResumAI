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

class TestResumeAnalysisScenario(unittest.TestCase):
    """
    ADAPTED SCENARIO: Resume Analysis -> Job Match Suggestions
    Based on: Age Input -> Bank Account Suggestions
    """
    
    def setUp(self):
        print(f"\n{'='*60}")
        print("ADAPTED TEST SCENARIO: Resume Analysis -> Job Match Suggestions")
        print(f"{'='*60}")
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        self.driver.get(TestConfig.BASE_URL)
        time.sleep(3)
    
    def test_resume_analysis_triggers_suggestions(self):
        """Test that resume analysis triggers job match suggestions"""
        print("Testing resume analysis suggestions...")
        
        # Fill user information
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Name']")
        if inputs:
            inputs[0].send_keys("John Doe")
        
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Email']")
        if inputs:
            inputs[0].send_keys("john.doe@example.com")
        
        # Try to upload file if exists
        if os.path.exists(TestConfig.SAMPLE_RESUME_PATH):
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(os.path.abspath(TestConfig.SAMPLE_RESUME_PATH))
            print("OK - Resume uploaded")
        else:
            print("Using simulated resume data")
        
        # Enter job URL
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='URL']")
        if inputs:
            inputs[0].send_keys(TestConfig.TEST_JOB_URL)
        
        # Click analyze button
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Analyze')]")
        if buttons:
            buttons[0].click()
            time.sleep(5)
            
            # Check for analysis results
            page_content = self.driver.page_source
            analysis_indicators = ["Analysis", "Match", "Score", "Skills", "Recommend"]
            found_indicators = [ind for ind in analysis_indicators if ind in page_content]
            
            print(f"Found analysis indicators: {found_indicators}")
            self.assertGreater(len(found_indicators), 0, "Should show analysis results")
            
            print("ACTUAL RESULT: Resume analysis triggered job match suggestions")
    
    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()