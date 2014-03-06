#!/bin/bash
set -e
set -x
DOCKER_ARGS=""
PROGRAM_ARGS="test_loopback"
DOCKERFILE="Dockertests"

cp $DOCKERFILE Dockerfile
docker build -t tctest .
rm -rf /tmp/sonar-reports
if [ -f CIDFILE ]; then
    rm CIDFILE
fi

echo "Killing old docker"
docker stop $(docker ps -a -q) || true
docker rm $(docker ps -a -q) || true

REPORTS_PATH=`pwd`"/sonar-reports"
mkdir -p $REPORTS_PATH
docker run -e COVERAGE_FILE="/sonar-reports/coverage" -v $REPORTS_PATH:/sonar-reports -p 55556:55555 -cidfile=CIDFILE -i -t tctest  $PROGRAM_ARGS &
while ! nc -z 127.0.0.1 55556; do sleep 1; echo "Waiting for local port to open"; done
killall ngrok || true
ngrok -log=stdout -proto=tcp 55556 > ngrok.log &
sleep 5 #we assume the tunnel is setup at this point
cat ngrok.log | grep "Tunnel established at" | grep -oEi "[A-Za-z\.]+:[0-9]+" > CAFFEINE_SERVER
echo "caffeine server is available at"
cat CAFFEINE_SERVER
echo "##teamcity[publishArtifacts 'CAFFEINE_SERVER']"
docker ps
docker logs $( docker ps -q )
echo "##teamcity[publishArtifacts 'ngrok.log']"
