#!/usr/bin/env bash

qualityGateUrl="${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${SONAR_PROJETCKEY}"
qualityGateStatus="$(curl --silent --fail --show-error --user "${SONAR_TOKEN}": "${qualityGateUrl}" | jq -r '.projectStatus.status')"

projectStatusUrl="${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${SONAR_PROJETCKEY}"
project_status="$(curl -s -u ${SONAR_TOKEN}: -G --data-urlencode --data-urlencode \
${projectStatusUrl})"

codeOk=$(jq -r '.projectStatus.conditions[] | select(.status=="OK") | "\n✅Status: " + .status, "MetricKey: " + .metricKey, "Comparator: " + .comparator, "ErrorThreshold: " + .errorThreshold, "ActualValue: " + .actualValue' <<< "$project_status")
codeOk="${codeOk//'%'/'%25'}"
codeOk="${codeOk//$'\n'/'%0A'}"
codeOk="${codeOk//$'\r'/'%0D'}"

codeFail=$(jq -r '.projectStatus.conditions[] | select(.status=="ERROR") | "\n💣Status: " + .status, "MetricKey: " + .metricKey, "Comparator: " + .comparator, "ErrorThreshold: " + .errorThreshold, "ActualValue: " + .actualValue' <<< "$project_status")
codeFail="${codeFail//'%'/'%25'}"
codeFail="${codeFail//$'\n'/'%0A'}"
codeFail="${codeFail//$'\r'/'%0D'}"

error="ERROR CONFIGURATION"

codeValidation () {

if [[ ${qualityGateStatus} == "OK" ]]; then
     echo "👋 Hey Quality Gate has PASSED.$codeOk"
elif [[ ${qualityGateStatus} == "ERROR" ]]; then
     echo "👋 Hey Quality Gate has FAILED.$codeFail"
else
   echo "::set-output name=quality_check::$error"
fi
}

result=$(codeValidation)
# echo "::set-output name=quality_check::$result"

echo "quality_check=result" >> $GITHUB_OUTPUT

