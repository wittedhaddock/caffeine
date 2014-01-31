

import unittest
if __name__ == '__main__':
    import sys
    print (sys.argv)
    if "--teamcity" in sys.argv:
        from teamcity.unittestpy import TeamcityTestRunner
        runner = TeamcityTestRunner()
    elif "--coverage" in sys.argv:
        import xmlrunner
        import os.path
        if not os.path.exists('/xunit-reports'): os.path.mkdir('/xunit-reports')
        runner = xmlrunner.XMLTestRunner(output='/xunit-reports')
    else:
        runner = unittest.TextTestRunner()
    testsuite = unittest.TestLoader().discover('.')
    runner.run(testsuite)