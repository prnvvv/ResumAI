"""Configuration for all tests"""

class TestConfig:
    # Application URL
    BASE_URL = "http://localhost:8501"
    
    # Timeouts
    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_TIMEOUT = 20
    
    # Performance thresholds
    MAX_PAGE_LOAD_TIME = 10
    MAX_MEMORY_USAGE = 500
    
    # File paths
    SAMPLE_RESUME_PATH = "tests/test_data/sample_resume.pdf"
    
    # Test data
    TEST_USER = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    
    TEST_JOB_URL = "https://example.com/job-posting"