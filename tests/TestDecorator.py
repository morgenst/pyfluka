import unittest
from collections import OrderedDict
from base.StoredData import StoredData
from plugins.Decorator import Decorator
from utils import PhysicsQuantities as PQ
from reader import _dh


class TestDecorator(unittest.TestCase):
    def setUp(self):
        self.decorator = Decorator(["EInh"])
        self.data = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.)))])}

    def test_config_parse(self):
        self.assertEqual(self.decorator.config, ["EInh"])

    def test_config_parse_builin(self):
        self.assertEqual(self.decorator.quantities, [_dh._einh])

    def test_invoke(self):
        self.decorator.invoke(self.data)
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.),
                                                                     PQ.EInh(4.10E-011)))])}
        self.assertEqual(self.data, res)
