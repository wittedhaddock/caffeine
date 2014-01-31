echo "0"
coverage run tests.py --sonar
echo "1"
mkdir coverage-reports
echo "2"
coverage xml -i -o coverage-reports/coverage-tests.xml
echo "3"