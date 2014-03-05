#!/bin/bash
DOCKER_ARGS=""
PROGRAM_ARGS="test_loopback"
DOCKERFILE="Dockertests"

cp $DOCKERFILE Dockerfile
docker build -t tctest .
rm -rf /tmp/sonar-reports
if [ -f CIDFILE ]; then
    rm CIDFILE
fi

#figure out hostname of docker instance
if [ -n $DOCKER_HOST ]; then
	DOCKER_HN=$( echo "$DOCKER_HOST" | grep -oE '((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])' )
else
	DOCKER_HN="127.0.0.1"
fi
REPORTS_PATH="/tmp/sonar-reports"
mkdir -p $REPORTS_PATH
docker run -e COVERAGE_FILE="sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports -p 55555:55555 -cidfile=CIDFILE -i -t tctest  $PROGRAM_ARGS &

while ! nc -vz $DOCKER_HN 55555; do sleep 1; echo "Waiting for port to open"; done

