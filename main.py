import os
import requests
from github import Github

# Configuration of environment variables
SONAR_HOST_URL = os.getenv('SONAR_HOST_URL')
SONAR_PROJECTKEY = os.getenv('SONAR_PROJECTKEY')
SONAR_TOKEN = os.getenv('SONAR_TOKEN')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # GitHub token
REPO_NAME = os.getenv('GITHUB_REPOSITORY')  # Ex: "user/repository"
PR_NUMBER = os.getenv('PR_NUMBER')  # Pull Request number

def get_quality_gate_status():
    quality_gate_url = f"{SONAR_HOST_URL}/api/qualitygates/project_status?projectKey={SONAR_PROJECTKEY}"
    # Make the request to the SonarQube API
    response = requests.get(quality_gate_url, auth=(SONAR_TOKEN, ''))
    response.raise_for_status()
    
    project_status = response.json()
    quality_gate_status = project_status['projectStatus']['status']
    
    print(f"Quality gate status retrieved: {quality_gate_status}")
    return quality_gate_status, project_status

def extract_code_details(project_status):
    # Extract all conditions regardless of their status
    conditions = project_status['projectStatus']['conditions']

    # Start creating a Markdown table
    table = "\n| **Metric** | **Value** |\n|------------|-----------|\n"
    
    # Fill the table with metric details
    for condition in conditions:
        metric = condition['metricKey'].replace('_', ' ')
        actual_value = condition['actualValue']
        if isinstance(actual_value, float):
            actual_value = f"{actual_value:.1f}"  # Format floats to 1 decimal place
        table += f"| {metric} | {actual_value} |\n"
    
    return table

def code_validation():
    quality_gate_status, project_status = get_quality_gate_status()

    # Construct the result with the overall status and the detailed metrics table
    status_emoji = '✅' if quality_gate_status == "OK" else '💣'
    result = f"{status_emoji} **Status: {quality_gate_status}**\n"
    details_table = extract_code_details(project_status)
    result += details_table

    return result

def comment_on_pull_request(body):
    # Authenticate with GitHub
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    pull_request = repo.get_pull(int(PR_NUMBER))

    print(f"Commenting on Pull Request #{PR_NUMBER}.")
    # Comment on the Pull Request
    pull_request.create_issue_comment(body)

if __name__ == "__main__":
    # Execute code validation
    result = code_validation()
    
    # Comment on the Pull Request
    if GITHUB_TOKEN and REPO_NAME and PR_NUMBER:
        comment_on_pull_request(result)
    else:
        print("Error: GitHub token, repository, or PR number not configured.")
