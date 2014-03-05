#!/bin/bash
CID=$(cat CIDFILE)
#docker stop $CID
rm CIDFILE
REPORTS_PATH="/tmp/sonar-reports"
#docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports -cidfile=CIDFILE -t tctest --teamcity
#docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports -t tctest --sonar
docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports --entrypoint="coverage-3.3" -t tctest  xml -i -o sonar-reports/coverage.xml

echo "##teamcity[publishArtifacts '<path>']"


