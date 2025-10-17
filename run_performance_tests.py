import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tests.performance.test_performance import PerformanceTests

def run_performance_tests():
    """Run performance tests"""
    print("🚀 Running Performance Tests")
    print("=" * 50)
    
    try:
        perf_tester = PerformanceTests()
        perf_tester.run_all_performance_tests()
        return 0
    except Exception as e:
        print(f"❌ Performance tests failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_performance_tests())