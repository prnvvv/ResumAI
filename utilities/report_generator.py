"""Generate test reports"""
import json
import os
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_html_report(test_results, report_type="comprehensive"):
        """Generate HTML test report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"results/html_reports/{report_type}_report_{timestamp}.html"
        os.makedirs("results/html_reports", exist_ok=True)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
                .test-result {{ margin: 10px 0; padding: 10px; border-left: 5px solid; }}
                .pass {{ border-color: green; background: #e8f5e8; }}
                .fail {{ border-color: red; background: #ffe8e8; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ATS Resume Analyzer - Test Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        for test_name, result in test_results.items():
            status_class = "pass" if result.get('passed', False) else "fail"
            status_emoji = "✅" if result.get('passed', False) else "❌"
            
            html_content += f"""
            <div class="test-result {status_class}">
                <h3>{status_emoji} {test_name}</h3>
                <p>Status: {"PASS" if result.get('passed') else "FAIL"}</p>
            </div>
            """
        
        html_content += "</body></html>"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file