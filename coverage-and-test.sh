echo "0"
cd caffeine && coverage run tests.py --sonar
cd ..
mv caffeine/xunit-reports .
echo "1"
mkdir coverage-reports
echo "2"
coverage xml -i -o coverage-reports/coverage-tests.xml
echo "3"