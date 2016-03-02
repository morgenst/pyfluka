import unittest
import base.AnalysisBase as BC

class testBaseCycle(unittest.TestCase):
    def setUp(self):
        pass

    def testConfigParse(self):
        bc = BC.AnalysisBase(None, "testconfig.yaml")
        bc._loadConfig()

    def testConfigParseFail(self):
        bc = BC.AnalysisBase(None, "nonexisting.yaml")
        self.assertRaises(IOError, bc._loadConfig)

    def testConfigParse(self):
        bc = BC.AnalysisBase(None, "testconfig.yaml")
        bc.setup()
