import sys
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def check_setup():
    print("🔍 Debugging Setup Issues...")
    print("=" * 50)
    
    issues = []
    
    # Check 1: Streamlit app running
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit app is running on port 8501")
        else:
            print(f"❌ Streamlit app returned status: {response.status_code}")
            issues.append("Streamlit app not accessible")
    except requests.exceptions.RequestException as e:
        print(f"❌ Streamlit app not running: {e}")
        issues.append("Streamlit app not running")
    
    # Check 2: Selenium setup
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.quit()
        print("✅ Selenium Chrome driver working")
    except Exception as e:
        print(f"❌ Selenium setup failed: {e}")
        issues.append("Selenium setup failed")
    
    # Check 3: Test files exist
    test_files = [
        "tests/test_data/sample_resume.pdf",
        "tests/functional/test_ats_analyzer.py",
        "config/test_config.py"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ File missing: {file_path}")
            issues.append(f"Missing file: {file_path}")
    
    # Check 4: Required packages
    required_packages = ['selenium', 'webdriver_manager', 'requests', 'psutil']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package installed: {package}")
        except ImportError:
            print(f"❌ Package missing: {package}")
            issues.append(f"Missing package: {package}")
    
    print("\n" + "=" * 50)
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All checks passed! Setup is ready.")
        return True

if __name__ == "__main__":
    check_setup()