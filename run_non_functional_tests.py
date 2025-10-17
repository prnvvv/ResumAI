import unittest
import sys
import os

def run_non_functional_tests():
    """Run all non-functional tests"""
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
    print(f"\nNON-FUNCTIONAL TESTS SUMMARY")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_non_functional_tests()
    sys.exit(0 if success else 1)