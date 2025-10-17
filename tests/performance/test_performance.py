import time
import threading
import requests
import psutil
import os
import json
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.test_config import TestConfig

class PerformanceTests:
    
    def __init__(self):
        self.base_url = TestConfig.BASE_URL
        self.results_dir = "results/performance_reports"
        os.makedirs(self.results_dir, exist_ok=True)
        self.results = {}
    
    def test_page_load_performance(self):
        """Test page load performance"""
        print("Testing page load performance...")
        
        load_times = []
        for i in range(3):
            start_time = time.time()
            try:
                response = requests.get(self.base_url, timeout=TestConfig.PAGE_LOAD_TIMEOUT)
                end_time = time.time()
                
                if response.status_code == 200:
                    load_time = end_time - start_time
                    load_times.append(load_time)
                    print(f"  Load {i+1}: {load_time:.2f}s")
                else:
                    print(f"  Load {i+1}: Failed (HTTP {response.status_code})")
                    
            except Exception as e:
                print(f"  Load {i+1}: Error ({str(e)})")
            
            time.sleep(1)
        
        if load_times:
            avg_load_time = sum(load_times) / len(load_times)
            self.results['page_load_performance'] = {
                'average': avg_load_time,
                'min': min(load_times),
                'max': max(load_times)
            }
            
            print(f"OK - Average page load: {avg_load_time:.2f}s")
            return avg_load_time
        return None
    
    def test_memory_usage(self):
        """Test memory consumption"""
        print("Testing memory usage...")
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        # Simulate operations
        data = []
        for i in range(3):
            data.append([j for j in range(50000)])
            time.sleep(0.5)
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_used = final_memory - initial_memory
        
        self.results['memory_usage'] = {
            'initial_mb': initial_memory,
            'final_mb': final_memory,
            'used_mb': memory_used
        }
        
        print(f"OK - Memory usage: {memory_used:.2f}MB")
        return memory_used
    
    def save_performance_report(self):
        """Save performance results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{self.results_dir}/performance_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"OK - Performance report saved: {report_file}")
        return report_file
    
    def run_all_performance_tests(self):
        """Run all performance tests"""
        print("Starting Performance Test Suite")
        print("=" * 60)
        
        try:
            self.test_page_load_performance()
            time.sleep(2)
            
            self.test_memory_usage()
            
            self.save_performance_report()
            
            print("\nPerformance tests completed successfully!")
            
        except Exception as e:
            print(f"Performance test failed: {e}")
            self.save_performance_report()
            raise

if __name__ == "__main__":
    perf_tester = PerformanceTests()
    perf_tester.run_all_performance_tests()