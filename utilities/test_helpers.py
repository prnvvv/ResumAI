"""Helper functions for tests"""
import os
from datetime import datetime
from selenium.webdriver.common.by import By

class TestHelpers:
    @staticmethod
    def take_screenshot(driver, test_name):
        """Take screenshot and save with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/screenshots/{test_name}_{timestamp}.png"
        os.makedirs("results/screenshots", exist_ok=True)
        driver.save_screenshot(filename)
        return filename
    
    @staticmethod
    def fill_form_field(driver, placeholder_text, value):
        """Fill form field by placeholder"""
        elements = driver.find_elements(By.CSS_SELECTOR, f"input[placeholder*='{placeholder_text}']")
        if elements:
            elements[0].clear()
            elements[0].send_keys(value)
            return True
        return False