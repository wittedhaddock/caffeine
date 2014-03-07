

import unittest
import os
import sys
import os.path
sys.path.append(os.path.abspath("caffeine"))

if __name__ == '__main__':
    import sys
    print (sys.argv)
    if "--teamcity" in sys.argv:
        from teamcity.unittestpy import TeamcityTestRunner
        runner = TeamcityTestRunner()
    elif "--sonar" in sys.argv:
        sys.path.append("/caffeine/unittest-xml-reporting-master/src")# work around https://github.com/danielfm/unittest-xml-reporting/pull/46
        print (sys.path)

        import xmlrunner
        runner = xmlrunner.XMLTestRunner(output='/sonar-reports/')
    elif "test_loopback" in sys.argv:
        print ("Running loopback")
        from testMultiplatform import TestSequence
        TestSequence().test_loopback()
    else:
        print ("Nothing interesting in sys.argv.  Running standard tests.")
        runner = unittest.TextTestRunner()
    #import pdb
    #pdb.set_trace()
    testsuite = unittest.TestLoader().discover('tests')
    runner.run(testsuite)