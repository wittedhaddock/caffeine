from teamcity.unittestpy import TeamcityTestRunner

import unittest
if __name__ == '__main__':
    import sys
    if "--teamcity" in sys.argv:
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    testsuite = unittest.TestLoader().discover('.')
    runner.run(testsuite)