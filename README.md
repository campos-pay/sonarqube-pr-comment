# SonarQube Pull Request Comment

Check the Quality Gate of your code with [SonarQube](https://www.sonarqube.org/) to ensure your code meets your own quality standards before you release or deploy new features.

<img src="./images/SonarQube.png">

SonarQube is the leading product for Continuous Code Quality & Code Security. It supports most popular programming languages, including Java, JavaScript, TypeScript, C#, Python, C, C++, and many more.

## Requirements
Github Token secret is automatically created by Github, you just need to reference on your workflow.

A previous step must have run an analysis on your code.

Read more information on how to analyze your code [here](https://docs.sonarqube.org/latest/analysis/github-integration/)

## Usage

The workflow YAML file will usually look something like this::

```yaml
on:
  # Trigger analysis when pushing in master or pull requests, and when creating
  # a pull request. 
  push:
    branches:
      - main
  pull_request:
      types: [opened, synchronize, reopened]
name: Main Workflow
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with:
        # Disabling shallow clone is recommended for improving relevancy of reporting.
        fetch-depth: 0

    # Triggering SonarQube analysis as results of it are required by Quality Gate check.
    - name: SonarQube Scan
      uses: sonarsource/sonarqube-scan-action@master
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

    # Check the Quality Gate status.
    - name: SonarQube Quality Gate check
      id: sonarqube-quality-gate-check
      uses: sonarsource/sonarqube-quality-gate-action@master
      # Force to fail step after specific time.
      timeout-minutes: 5
      env:
       SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
       SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }} #OPTIONAL

     - name: Get Sonar Status and PR Comment
       if: always()
       uses: campos-pay/sonarqube-pr-comment@main
       with:
         SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
         SONAR_URL: ${{ secrets.SONAR_HOST_URL }}
         SONAR_PROJETCKEY: my-app
         GITHUB-TOKEN: ${{ secrets.GITHUB_TOKEN }}

```
## Example Result
For result Ok 

<img src="./images/result-ok.png">

For failed result

<img src="./images/result-fail.png">
