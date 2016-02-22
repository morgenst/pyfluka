import unittest
import base.BaseCycle as BC

class testBaseCycle(unittest.TestCase):
    def setUp(self):
        pass

    def testConfigParse(self):
        bc = BC.BaseCycle("testconfig.yaml")
        bc._loadConfig()

    def testConfigParseFail(self):
        bc = BC.BaseCycle("nonexisting.yaml")
        self.assertRaises(IOError, bc._loadConfig)

    def testConfigParse(self):
        bc = BC.BaseCycle("testconfig.yaml")
        bc.setup()
