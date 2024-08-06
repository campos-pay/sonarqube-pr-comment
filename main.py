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
GITHUB_API_BASE_URL = os.getenv('GITHUB_API_BASE_URL') or None

def get_quality_gate_status():
    quality_gate_url = f"{SONAR_HOST_URL}/api/qualitygates/project_status?projectKey={SONAR_PROJECTKEY}"
    # Make the request to the SonarQube API
    response = requests.get(quality_gate_url, auth=(SONAR_TOKEN, ''))
    response.raise_for_status()
    
    project_status = response.json()
    quality_gate_status = project_status['projectStatus']['status']
    
    print(f"Quality gate status retrieved: {quality_gate_status}")
    return quality_gate_status, project_status

def extract_code_details(project_status, status_filter):
    # Filter conditions based on status ("OK" or "ERROR")
    conditions = project_status['projectStatus']['conditions']
    filtered_conditions = [condition for condition in conditions if condition['status'] == status_filter]

    # Create formatted strings with details of the filtered conditions
    details = [
        f"\n{'✅' if status_filter == 'OK' else '💣'}Status: {condition['status']}, \n"
        f"MetricKey: {condition['metricKey']}\n"
        f"Comparator: {condition['comparator']}\n"
        f"ErrorThreshold: {condition['errorThreshold']}\n"
        f"ActualValue: {condition['actualValue']}\n"
        for condition in filtered_conditions
    ]
    
    return ''.join(details)

def code_validation():
    quality_gate_status, project_status = get_quality_gate_status()

    if quality_gate_status == "OK":
        code_ok = extract_code_details(project_status, "OK")
        result = f"👋 Hey, the Quality Gate has PASSED.{code_ok}"
    elif quality_gate_status == "ERROR":
        code_fail = extract_code_details(project_status, "ERROR")
        result = f"👋 Hey, the Quality Gate has FAILED.{code_fail}"
    else:
        result = "quality_check=ERROR CONFIGURATION"

    return result

def comment_on_pull_request(body, base_url=None):
    # Authenticate with GitHub
    if base_url is not None:
        g = Github(GITHUB_TOKEN, base_url=base_url)
    else:
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
        comment_on_pull_request(result, base_url=GITHUB_API_BASE_URL)
    else:
        print("Error: GitHub token, repository, or PR number not configured.")
