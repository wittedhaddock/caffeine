from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner

import unittest

if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    testsuite = unittest.TestLoader().discover('.')
    runner.run(testsuite)