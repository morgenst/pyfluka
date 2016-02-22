__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
from utils.OrderedYAMLExtension import dump
from base import ConfigParser
from collections import OrderedDict


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.f = open("test.yaml", "w")
        self.f2 = open("test2.yaml", "w")
        self.data = {"a": [1, 2, 3]}
        self.data2 = {"a": [1, 2, 3, 4]}
        self.data3 = {"plugins" : OrderedDict([(1,0), (3,1), (2,4)])}
        dump(self.data, self.f)
        dump(self.data3, self.f2)

    def tearDown(self):
        self.f.close()
        import os
        os.remove("test.yaml")
        os.remove("test2.yaml")

    def test_NonExistingFile(self):
        self.assertRaises(IOError, ConfigParser.parse, "")

    def test_parseConfig(self):
        d = ConfigParser.parse("test.yaml")
        self.assertEqual(d, self.data)

    def test_falseParse(self):
        d = ConfigParser.parse("test.yaml")
        self.assertNotEqual(d, self.data2)

    def test_parseOrder(self):
        od = ConfigParser.parse("test2.yaml")
        res = [1,2,3]
        self.assertEqual(od['plugins'].keys(), res)

if __name__ == '__main__':
    unittest.main()