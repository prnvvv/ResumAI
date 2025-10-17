# Agile Tools & Methodology Implementation

## (ii) Agile Tools Applied During Development & Testing

### JIRA for Project Management
- **Backlog Management**: User stories organized into epics (Authentication, Resume Analysis, Reporting, Testing)
- **Sprint Planning**: 2-week sprints with capacity planning and velocity tracking (30 story points per sprint)
- **Task Tracking**: Kanban board with columns (To Do, In Progress, Code Review, Testing, Done)
- **Continuous Integration**: JIRA integration with GitHub Actions for automated test execution on every commit
- **Collaboration**: @mentions for team communication, file attachments for design documents, comments for decision tracking

### Azure DevOps Pipeline
```yaml
# azure-pipelines.yml
trigger:
- main
- develop

stages:
- stage: Test
  jobs:
  - job: FunctionalTests
    steps:
    - script: |
        pip install -r requirements.txt
        python run_all_tests.py
      displayName: 'Run Complete Test Suite'
  
  - job: PerformanceTests
    steps:
    - script: |
        python run_performance_tests.py
      displayName: 'Run Performance Tests'
  
  - job: SecurityTests
    steps:
    - script: |
        python tests/performance/test_security.py
      displayName: 'Run Security Tests'

- stage: Deploy
  jobs:
  - job: DeployToStaging
    steps:
    - script: |
        echo "Deploying to staging environment..."