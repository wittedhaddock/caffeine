FROM drewcrawford/caffeinebase
MAINTAINER drew

#run router
ADD . .
EXPOSE 55555 55555

ENTRYPOINT python3.3 tests.py

