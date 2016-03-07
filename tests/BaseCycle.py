import unittest
import base.AnalysisBase as BC


class TestBaseCycle(unittest.TestCase):
    def setUp(self):
        pass

    def testConfigParse(self):
        bc = BC.AnalysisBase(None, "testconfig.yaml")
        bc._loadConfig()

    def testConfigParseFail(self):
        bc = BC.AnalysisBase(None, "nonexisting.yaml")
        self.assertRaises(IOError, bc._loadConfig)

    @unittest.skip("What was this test suppose to do?")
    def testConfigParse2(self):
        bc = BC.AnalysisBase(None, "testconfig.yaml")
        bc.setup()

    @unittest.skip("Not implemented")
    def testNonExistingInputFileException(self):
        pass
