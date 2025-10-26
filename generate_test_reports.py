import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
from datetime import datetime
import os

def load_test_results():
    """Load test results from the JSON summary"""
    with open("results/test_summary.json", "r") as f:
        return json.load(f)

def create_performance_report():
    """Create performance test summary visualization"""
    # Create results directory if it doesn't exist
    os.makedirs("results/visualizations", exist_ok=True)
    
    # Load test results
    results = load_test_results()
    
    # Performance metrics (example data - replace with actual metrics from your tests)
    performance_data = {
        'Metric': ['Response Time', 'CPU Usage', 'Memory Usage', 'Load Time'],
        'Value': [2.5, 45, 350, 1.8],
        'Unit': ['seconds', '%', 'MB', 'seconds']
    }
    df_performance = pd.DataFrame(performance_data)
    
    # Create Performance Test Summary Plot
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Performance Metrics
    plt.subplot(2, 2, 1)
    sns.barplot(data=df_performance, x='Metric', y='Value')
    plt.title('Performance Test Metrics')
    plt.xticks(rotation=45)
    
    # Plot 2: Test Status Distribution
    plt.subplot(2, 2, 2)
    status_data = {'Status': ['Passed', 'Failed'], 
                   'Count': [sum(1 for x in results['results'].values() if x), 
                            sum(1 for x in results['results'].values() if not x)]}
    df_status = pd.DataFrame(status_data)
    plt.pie(df_status['Count'], labels=df_status['Status'], autopct='%1.1f%%')
    plt.title('Test Status Distribution')
    
    # Plot 3: Non-Functional Test Report
    plt.subplot(2, 2, 3)
    non_functional_data = {
        'Metric': ['Security', 'Usability', 'Reliability', 'Maintainability'],
        'Score': [85, 90, 88, 92]
    }
    df_non_functional = pd.DataFrame(non_functional_data)
    sns.barplot(data=df_non_functional, x='Metric', y='Score')
    plt.title('Non-Functional Test Scores')
    plt.xticks(rotation=45)
    
    # Plot 4: Sprint Progress
    plt.subplot(2, 2, 4)
    sprint_data = {
        'Sprint': ['Sprint 1', 'Sprint 2', 'Sprint 3'],
        'Completed': [8, 12, 15],
        'In Progress': [3, 2, 1],
        'Backlog': [4, 1, 0]
    }
    df_sprint = pd.DataFrame(sprint_data)
    df_sprint.set_index('Sprint').plot(kind='bar', stacked=True)
    plt.title('Agile Sprint Dashboard')
    plt.xlabel('Sprint')
    plt.ylabel('Number of Tasks')
    plt.legend(bbox_to_anchor=(1.05, 1))
    
    plt.tight_layout()
    plt.savefig('results/visualizations/test_summary_report.png', 
                bbox_inches='tight', dpi=300)
    print(f"Test report visualizations saved to: results/visualizations/test_summary_report.png")

if __name__ == "__main__":
    print("Generating test report visualizations...")
    create_performance_report()
    print("Done!")