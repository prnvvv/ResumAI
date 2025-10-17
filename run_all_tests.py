import os
import sys
import subprocess
import json
from datetime import datetime

def run_tests():
    """Run all test suites"""
    print("Starting Comprehensive Test Suite")
    print("=" * 60)
    
    # Create results directory
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/screenshots", exist_ok=True)
    os.makedirs("results/performance_reports", exist_ok=True)
    
    test_results = {}
    
    try:
        # 1. Run Functional Tests
        print("\n1. RUNNING FUNCTIONAL TESTS")
        print("-" * 40)
        result = subprocess.run([
            sys.executable, "-m", "unittest", "discover", 
            "tests/functional", "-v"
        ], capture_output=True, text=True)
        
        test_results['functional'] = result.returncode == 0
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # 2. Run Performance Tests
        print("\n2. RUNNING PERFORMANCE TESTS")
        print("-" * 40)
        result = subprocess.run([
            sys.executable, "tests/performance/test_performance.py"
        ], capture_output=True, text=True)
        
        test_results['performance'] = result.returncode == 0
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
    except Exception as e:
        print(f"Error running tests: {e}")
        test_results['error'] = str(e)
    
    # Generate final report
    print("\n" + "=" * 60)
    print("TEST SUITE SUMMARY")
    print("=" * 60)
    
    for test_type, passed in test_results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_type.upper():<15} {status}")
    
    print("=" * 60)
    
    # Save overall results
    with open("results/test_summary.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": test_results
        }, f, indent=2)
    
    # Return overall success
    all_passed = all(result for result in test_results.values() if isinstance(result, bool))
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_tests())