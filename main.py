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

def get_sonar_measures():
    measures_url = f"{SONAR_HOST_URL}/api/measures/component?component={SONAR_PROJECTKEY}&metricKeys=security_hotspots_reviewed,duplicated_lines_density,lines,coverage,security_hotspots,lines_to_cover,bugs,code_smells,vulnerabilities"
    response = requests.get(measures_url, auth=(SONAR_TOKEN, ''))
    response.raise_for_status()
    
    measures = response.json()
    print(f"Métricas do SonarQube recuperadas: {measures}")
    return measures['component']['measures']

def format_measures_to_table(measures):
    # Inicia a criação de uma tabela em Markdown
    table = "\n| **Métrica** | **Valor** |\n|------------|-----------|\n"
    
    # Preenche a tabela com os detalhes das métricas
    for measure in measures:
        metric = measure['metric'].replace('_', ' ')
        value = measure['value']
        table += f"| {metric} | {value} |\n"
    
    return table

def code_validation():
    measures = get_sonar_measures()
    details_table = format_measures_to_table(measures)
    
    # Cria o resultado final com a tabela das métricas
    result = f"✅ **Status: OK**\n{details_table}"
    
    return result

def comment_on_pull_request(body):
    # Autentica com o GitHub
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    pull_request = repo.get_pull(int(PR_NUMBER))

    print(f"Comentando na Pull Request #{PR_NUMBER}.")
    # Comenta na Pull Request
    pull_request.create_issue_comment(body)

if __name__ == "__main__":
    # Execute code validation
    result = code_validation()
    
    # Comment on the Pull Request
    if GITHUB_TOKEN and REPO_NAME and PR_NUMBER:
        comment_on_pull_request(result)
    else:
        print("Error: GitHub token, repository, or PR number not configured.")
