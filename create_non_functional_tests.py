import os
import shutil

def create_non_functional_tests():
    """Create the non-functional tests directory structure"""
    print("Setting up Non-Functional Tests")
    print("=" * 50)
    
    # Create directory structure
    directories = [
        "tests/non_functional",
        "tests/test_data",
        "results/non_functional_reports"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created: {directory}")
    
    # Create placeholder test files WITHOUT UNICODE CHARACTERS
    test_files = {
        "tests/non_functional/test_scalability.py": """
import unittest

class TestScalability(unittest.TestCase):
    def test_concurrent_users(self):
        \"\"\"Test application with multiple concurrent users\"\"\"
        self.skipTest("Scalability tests not implemented yet")
        
    def test_large_file_handling(self):
        \"\"\"Test performance with large resume files\"\"\"
        self.skipTest("Large file handling tests not implemented yet")
""",
        
        "tests/non_functional/test_reliability.py": """
import unittest

class TestReliability(unittest.TestCase):
    def test_extended_usage(self):
        \"\"\"Test application stability over extended period\"\"\"
        self.skipTest("Reliability tests not implemented yet")
        
    def test_error_recovery(self):
        \"\"\"Test application recovery from errors\"\"\"
        self.skipTest("Error recovery tests not implemented yet")
""",
        
        "tests/non_functional/test_security.py": """
import unittest

class TestSecurity(unittest.TestCase):
    def test_file_upload_security(self):
        \"\"\"Test security of file upload functionality\"\"\"
        self.skipTest("Security tests not implemented yet")
        
    def test_xss_vulnerability(self):
        \"\"\"Test for Cross-Site Scripting vulnerabilities\"\"\"
        self.skipTest("XSS tests not implemented yet")
        
    def test_data_privacy(self):
        \"\"\"Test that sensitive data is not exposed\"\"\"
        self.skipTest("Data privacy tests not implemented yet")
""",
        
        "tests/non_functional/test_compatibility.py": """
import unittest

class TestCompatibility(unittest.TestCase):
    def test_cross_browser_compatibility(self):
        \"\"\"Test application across different browsers\"\"\"
        self.skipTest("Cross-browser tests not implemented yet")
        
    def test_mobile_responsiveness(self):
        \"\"\"Test application on mobile viewport\"\"\"
        self.skipTest("Mobile responsiveness tests not implemented yet")
""",
        
        "tests/non_functional/test_usability.py": """
import unittest

class TestUsability(unittest.TestCase):
    def test_navigation_efficiency(self):
        \"\"\"Test how quickly users can complete tasks\"\"\"
        self.skipTest("Usability tests not implemented yet")
        
    def test_error_message_clarity(self):
        \"\"\"Test that error messages are user-friendly\"\"\"
        self.skipTest("Error message tests not implemented yet")
""",
        
        "tests/non_functional/test_advanced_performance.py": """
import unittest

class TestAdvancedPerformance(unittest.TestCase):
    def test_memory_leaks(self):
        \"\"\"Test for memory leaks during extended use\"\"\"
        self.skipTest("Memory leak tests not implemented yet")
        
    def test_cpu_usage(self):
        \"\"\"Test CPU usage during intensive operations\"\"\"
        self.skipTest("CPU usage tests not implemented yet")
""",
        
        "run_non_functional_tests.py": """
import unittest
import sys
import os

def run_non_functional_tests():
    \"\"\"Run all non-functional tests\"\"\"
    print("Running Comprehensive Non-Functional Tests")
    print("=" * 50)
    
    # Add tests directory to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    
    # Discover and run non-functional tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests/non_functional', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate report
    print(f"\\nNON-FUNCTIONAL TESTS SUMMARY")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_non_functional_tests()
    sys.exit(0 if success else 1)
"""
    }
    
    for file_path, content in test_files.items():
        try:
            with open(file_path, 'w', encoding='utf-8') as f:  # Added encoding
                f.write(content.strip())
            print(f"Created: {file_path}")
        except Exception as e:
            print(f"Error creating {file_path}: {e}")
    
    print("\\nNon-functional tests setup complete!")
    print("Next steps:")
    print("  1. Implement the actual test logic in each test file")
    print("  2. Run: python run_all_tests.py")
    print("  3. Check results in results/non_functional_reports/")

if __name__ == "__main__":
    create_non_functional_tests()