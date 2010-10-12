import sys
import unittest
import test_update
import test_addfiles
import test_deletefiles
import test_revertfiles
import test_difffiles
import test_init_package
import test_init_project
import test_commit
import test_repairwc

suite = unittest.TestSuite()
suite.addTests(test_addfiles.suite())
suite.addTests(test_deletefiles.suite())
suite.addTests(test_revertfiles.suite())
suite.addTests(test_update.suite())
suite.addTests(test_difffiles.suite())
suite.addTests(test_init_package.suite())
suite.addTests(test_init_project.suite())
suite.addTests(test_commit.suite())
suite.addTests(test_repairwc.suite())
result = unittest.TextTestRunner(verbosity=1).run(suite)
sys.exit(not result.wasSuccessful())