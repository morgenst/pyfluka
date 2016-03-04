__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
import utils.PhysicsQuantities as PQ
from utils.OrderedYAMLExtension import dump
from base import ConfigParser, IllegalArgumentError
from collections import OrderedDict
from utils import ureg


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.f = open("test.yaml", "w")
        self.f2 = open("test2.yaml", "w")
        self.data = {"plugins": {"a": [1, 2, 3]}, "detectors": {"det1": {"mass": "100 kg"}}}
        self.data2 = {"plugin": {"a": [1, 2, 3, 4]}}
        self.data3 = {"plugins": OrderedDict([(1, 0), (3, 1), (2, 4)])}
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
        res = {"plugins": {"a": [1, 2, 3]}, "detectors": {"det1": {"mass": PQ.Mass(100, ureg.kg)}}}
        self.assertEqual(d, res)

    def test_falseParse(self):
        d = ConfigParser.parse("test.yaml")
        self.assertNotEqual(d, self.data2)

    def test_parseOrder(self):
        od = ConfigParser.parse("test2.yaml")
        res = [1, 3, 2]
        self.assertEqual(od['plugins'].keys(), res)

    def testAttrParsingTable(self):
        config = ConfigParser.parse("testconfig.yaml")
        res = {"plugins": {"AoverLECalculator": None, "TableMaker": {"cols": ["Isotope", "Activity", "AoverLE"]}}}
        self.assertEqual(config, res)

    def testAttrParsingPlot(self):
        config = ConfigParser.parse("testconfig_plot.yaml")
        res = {"plugins": {"PlotMaker": {"plots": {"activity": {"type": "2D", "quantity": "Activity"}}}}}
        self.assertEqual(config, res)

    def testInvalidInput(self):
        config = {"plugins": [{"PlotMaker": None}]}
        self.assertRaises(IllegalArgumentError, ConfigParser._validate, config)

    @unittest.skip("Not implemented")
    def testNonExistingPlugin(self):
        pass

    def testDetectorPassing(self):
        res = {"det1": {"mass": PQ.Mass(100., ureg.kg)}}
        config = ConfigParser.parse("test.yaml")
        self.assertEqual(config['detectors'], res)

if __name__ == '__main__':
    unittest.main()
