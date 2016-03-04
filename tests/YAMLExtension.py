import unittest
from collections import OrderedDict
from utils.OrderedYAMLExtension import dump


class TestYAMLExtension(unittest.TestCase):
    def setUp(self):
        self.d = OrderedDict([(1, 0), (3, 4), (5, 8), (2, 3)])

    def tearDown(self):
        import os
        os.remove("testoy.yaml")

    def testDump(self):
        f = open("testoy.yaml", "w")
        dump(self.d, f)
        f.close()
