import unittest
import requests
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simple_test():
    """Run a simple test to verify basic functionality"""
    print("🧪 Running Simple Test")
    print("=" * 40)
    
    # Test 1: Check if app is running
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        print(f"✅ App is running (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ App not accessible: {e}")
        return False
    
    # Test 2: Check if test files exist
    required_files = [
        "tests/functional/test_ats_analyzer.py",
        "tests/test_data/sample_resume.pdf",
        "config/test_config.py"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ File missing: {file_path}")
            all_files_exist = False
    
    if not all_files_exist:
        return False
    
    # Test 3: Run one simple unit test
    print("\n🔍 Running one functional test...")
    try:
        from tests.functional.test_ats_analyzer import TestATSResumeAnalyzer
        
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestATSResumeAnalyzer)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = simple_test()
    print("\n" + "=" * 40)
    if success:
        print("🎉 Simple test passed! You can now run full test suite.")
    else:
        print("❌ Simple test failed. Check the issues above.")
    sys.exit(0 if success else 1)