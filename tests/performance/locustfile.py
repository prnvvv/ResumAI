from locust import HttpUser, task, between
import random

class ATSResumeAnalyzerUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def load_main_page(self):
        self.client.get("/")
    
    @task(1)
    def simulate_analysis(self):
        # Simulate analysis request
        self.client.get("/")