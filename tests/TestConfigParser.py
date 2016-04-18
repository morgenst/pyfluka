__author__ = 'marcusmorgenstern'
__mail__ = ''

import os
import unittest
from collections import OrderedDict
from os.path import join

from pyfluka.base import IllegalArgumentError, _global_data
from pyfluka.utils import ureg
from pyfluka.utils.PhysicsQuantities import Mass

from pyfluka.base import ConfigParser
from pyfluka.utils.OrderedYAMLExtension import dump

_basedir = os.path.dirname(__file__)


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.f = open(join(_basedir, "test_data/test.yaml"), "w")
        self.f2 = open(join(_basedir, "test_data/test2.yaml"), "w")
        self.data = {"global": {"NoOfPrimaries": 10},
                     "plugins": {"a": [1, 2, 3]},
                     "detectors": {"det1": {"mass": "100 kg"}}}
        self.data2 = {"plugin": {"a": [1, 2, 3, 4]}}
        self.data3 = {"plugins": OrderedDict([(1, 0), (3, 1), (2, 4)])}
        dump(self.data, self.f)
        dump(self.data3, self.f2)
        _global_data._reset()

    def tearDown(self):
        self.f.close()
        os.remove(join(_basedir, "test_data/test.yaml"))
        os.remove(join(_basedir, "test_data/test2.yaml"))

    def test_NonExistingFile(self):
        self.assertRaises(IOError, ConfigParser.parse, "")

    def test_parseConfig(self):
        d = ConfigParser.parse(join(_basedir, "test_data/test.yaml"))
        res = {"plugins": {"a": [1, 2, 3]}}
        mass_res = {"det1": {"mass": Mass(100, ureg.kg)}, "NoOfPrimaries": 10}
        self.assertEqual(d, res)
        self.assertEqual(_global_data, mass_res)

    def test_falseParse(self):
        d = ConfigParser.parse(join(_basedir, "test_data/test.yaml"))
        self.assertNotEqual(d, self.data2)

    def test_parseOrder(self):
        od = ConfigParser.parse(join(_basedir, "test_data/test2.yaml"))
        res = [1, 3, 2]
        self.assertEqual(od['plugins'].keys(), res)

    def testAttrParsingTable(self):
        config = ConfigParser.parse(join(_basedir, "test_data/testconfig.yaml"))
        res = {"plugins": {"AoverLECalculator": None, "TableMaker": {"cols": ["Isotope", "Activity", "AoverLE"]}}}
        self.assertEqual(config, res)

    def testAttrParsingPlot(self):
        config = ConfigParser.parse(join(_basedir, "test_data/testconfig_plot.yaml"))
        res = {"plugins": {"PlotMaker": {"plots": {"activity": {"type": "2D", "quantity": "Activity"}}}}}
        self.assertEqual(config, res)

    def testInvalidInput(self):
        config = {"plugins": [{"PlotMaker": None}]}
        self.assertRaises(IllegalArgumentError, ConfigParser._validate, config)

    def test_non_existing_plugin_validate(self):
        config = {"det1": {"mass": Mass(100., ureg.kg)}, "NoOfPrimaries": 10}
        self.assertRaises(IllegalArgumentError, ConfigParser._validate, config)

    def test_non_existing_plugin_key_parse(self):
        config = {"det1": {"mass": "100 kg"}, "NoOfPrimaries": 10}
        f_config_name = join(_basedir, "test_data/config_no_plugin.yaml")
        f_config = open(f_config_name, "w")
        dump(config, f_config)
        f_config.close()
        self.assertRaises(IllegalArgumentError, ConfigParser.parse, f_config_name)
        os.remove(f_config_name)

    def test_non_existing_plugin_parse(self):
        config = {"plugins": ["foo", "bar"]}
        f_config_name = join(_basedir, "test_data/config_plugin_dict.yaml")
        f_config = open(f_config_name, "w")
        dump(config, f_config)
        f_config.close()
        self.assertRaises(IllegalArgumentError, ConfigParser.parse, f_config_name)
        os.remove(f_config_name)

    def test_detector_parsing(self):
        res = {"det1": {"mass": Mass(100., ureg.kg)}, "NoOfPrimaries": 10}
        config = ConfigParser.parse(join(_basedir, "test_data/test.yaml"))
        self.assertEqual(_global_data, res)

    def test_global_config_parsing(self):
        ConfigParser.parse(join(_basedir, "test_data/test.yaml"))
        self.assertEqual(_global_data["NoOfPrimaries"], 10.)

    def test_detector_parsing_types_global(self):
        config = {"global": {"NoOfPrimaries": "float:10"},
                  "plugins": {"a": [1, 2, 3]}}
        f_config_name = join(_basedir, "test_data/config_type_global.yaml")
        f_config = open(f_config_name, "w")
        dump(config, f_config)
        f_config.close()
        res = {"NoOfPrimaries": 10.}
        config = ConfigParser.parse(f_config_name)
        self.assertEqual(_global_data, res)
        os.remove(f_config_name)

if __name__ == '__main__':
    unittest.main()
