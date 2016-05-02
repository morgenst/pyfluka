import unittest
from pyfluka.base import InvalidInputError
from pyfluka.plugins.Filter import Filter
from pyfluka.utils import PhysicsQuantities as PQ
from pyfluka.utils import ureg
from pyfluka.base.StoredData import StoredData


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.config = {"quantity": "Activity", "threshold": 0.01}
        self.filter = Filter(**self.config)
        self.data = {"det1": {PQ.Isotope(3, 1, 0): StoredData(PQ.Activity(10.)),
                              PQ.Isotope(4, 2, 0): StoredData(PQ.Activity(2.)),
                              PQ.Isotope(22, 11, 0): StoredData(PQ.Activity(5.))}}

    def test_config_quantity(self):
        self.assertEqual(self.filter.quantity, "Activity")

    def test_config_threshold(self):
        self.assertEqual(self.filter.threshold, 0.01)

    def test_config_threshold_type(self):
        self.assertEqual(self.filter.type, "rel")

    def test_config_exception_no_quantity(self):
        config = {"threshold": 0.01}
        self.assertRaises(InvalidInputError, Filter, **config)

    def test_config_exception_no_threshold(self):
        config = {"quantity": "Activity"}
        self.assertRaises(InvalidInputError, Filter, **config)

    def test_config_absolute_threshold(self):
        config = {"quantity": "Activity", "threshold": "2.0 Bq"}
        fil = Filter(**config)
        self.assertEqual(fil.threshold, PQ.create_generic("ActivityThreshold", 2.0, 0., ureg.Bq))

    def test_absolute_filter_resnuc_data_single_pass(self):
        config = {"quantity": "Activity", "threshold": "8.0 Bq"}
        fil = Filter(**config)
        fil.invoke(self.data)
        self.assertEqual(self.data, {"det1": {PQ.Isotope(3, 1, 0): StoredData(PQ.Activity(10.))}})

    def test_absolute_filter_resnuc_data_none_pass(self):
        config = {"quantity": "Activity", "threshold": "11.0 Bq"}
        fil = Filter(**config)
        fil.invoke(self.data)
        self.assertEqual(self.data, {"det1": {}})

    def test_relative_filter_resnuc_data_single_pass(self):
        config = {"quantity": "Activity", "threshold": "0.5"}
        fil = Filter(**config)
        fil.invoke(self.data)
        self.assertEqual(self.data, {"det1": {PQ.Isotope(3, 1, 0): StoredData(PQ.Activity(10.))}})
