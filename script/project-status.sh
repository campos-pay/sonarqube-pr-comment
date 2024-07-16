#!/usr/bin/env bash

qualityGateUrl="${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${SONAR_PROJECTKEY}"
project_status=$(curl --silent --fail --show-error --user "${SONAR_TOKEN}": "${qualityGateUrl}")

qualityGateStatus=$(jq -r '.projectStatus.status' <<< "$project_status")

codeOk=$(jq -r '.projectStatus.conditions[] | select(.status=="OK") | "\n✅Status: " + .status, "MetricKey: " + .metricKey, "Comparator: " + .comparator, "ErrorThreshold: " + .errorThreshold, "ActualValue: " + .actualValue' <<< "$project_status")

codeFail=$(jq -r '.projectStatus.conditions[] | select(.status=="ERROR") | "\n💣Status: " + .status, "MetricKey: " + .metricKey, "Comparator: " + .comparator, "ErrorThreshold: " + .errorThreshold, "ActualValue: " + .actualValue' <<< "$project_status")

error="ERROR CONFIGURATION"

codeValidation () {
  if [[ ${qualityGateStatus} == "OK" ]]; then
    echo "👋 Hey, the Quality Gate has PASSED.$codeOk"
  elif [[ ${qualityGateStatus} == "ERROR" ]]; then
    echo "👋 Hey, the Quality Gate has FAILED.$codeFail"
  else
    echo "quality_check=${error}" >> $GITHUB_OUTPUT
  fi
}

result=$(codeValidation)

echo "quality_check<<EOF" >> $GITHUB_OUTPUT
echo "$result" >> $GITHUB_OUTPUT
echo "EOF" >> $GITHUB_OUTPUT


# #!/usr/bin/env bash

# qualityGateUrl="${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${SONAR_PROJECTKEY}"
# project_status=$(curl --silent --fail --show-error --user "${SONAR_TOKEN}": "${qualityGateUrl}")

# qualityGateStatus=$(jq -r '.projectStatus.status' <<< "$project_status")

# codeOk=$(jq -r '.projectStatus.conditions[] | select(.status=="OK") | "\n✅Status: " + .status, "MetricKey: " + .metricKey, "Comparator: " + .comparator, "ErrorThreshold: " + .errorThreshold, "ActualValue: " + .actualValue' <<< "$project_status")

# codeFail=$(jq -r '.projectStatus.conditions[] | select(.status=="ERROR") | "\n💣Status: " + .status, "MetricKey: " + .metricKey, "Comparator: " + .comparator, "ErrorThreshold: " + .errorThreshold, "ActualValue: " + .actualValue' <<< "$project_status")

# error="ERROR CONFIGURATION"

# codeValidation () {
#   if [[ "${qualityGateStatus}" == "OK" ]]; then
#     echo -e "👋 Hey, the Quality Gate has PASSED.${codeOk}"
#   elif [[ "${qualityGateStatus}" == "ERROR" ]]; then
#     echo -e "👋 Hey, the Quality Gate has FAILED.${codeFail}"
#   else
#     echo "quality_check=${error}"
#   fi
# }

# result=$(codeValidation)

# echo "quality_check=${result}" >> $GITHUB_ENV
