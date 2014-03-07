#!/bin/bash
set -e
CID=$(cat CIDFILE)
docker stop $CID
rm CIDFILE
REPORTS_PATH=`pwd`"/sonar-reports"
which pylint
docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports -cidfile=CIDFILE -t tctest --teamcity

rm -rf $REPORTS_PATH/TEST-*.xml
docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports -t tctest --sonar

docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports --entrypoint="coverage-3.3" -t tctest  xml -i -o /sonar-reports/coverage.xml
sed -i "s,filename=\"/caffeine/,filename=\"./,g" sonar-reports/coverage.xml

sonar-runner -X
echo "##teamcity[publishArtifacts 'sonar-reports']"


