import unittest
import base.AnalysisBase as BC


class TestAnalysisBase(unittest.TestCase):
    def setUp(self):
        pass

    def testConfigParse(self):
        bc = BC.AnalysisBase(None, "test_data/testconfig.yaml")
        bc._load_config()

    def testConfigParseFail(self):
        bc = BC.AnalysisBase(None, "test_data/nonexisting.yaml")
        self.assertRaises(IOError, bc._load_config)

    @unittest.skip("What was this test suppose to do?")
    def testConfigParse2(self):
        bc = BC.AnalysisBase(None, "test_data/testconfig.yaml")
        bc.setup()

    @unittest.skip("Not implemented")
    def testNonExistingInputFileException(self):
        pass

    @unittest.skip("Not implemented")
    def test_exception_plugin_creation(self):
        pass
