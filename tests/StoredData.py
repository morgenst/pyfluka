__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
from base import _global_data
from base.StoredData import StoredData
from math import sqrt
from collections import OrderedDict
from utils import PhysicsQuantities as PQ
from utils import ureg


class TestStoredData(unittest.TestCase):
    def setUp(self):
        self.singleElementData = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.)))])}

    def test_comparison(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.)))])}
        self.assertEqual(self.singleElementData, res)

    def test_comparison_unequal_different_magnitude(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(12., 2.)))])}
        self.assertNotEqual(self.singleElementData, res)

    def test_comparison_unequal_different_unc(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 3.)))])}
        self.assertNotEqual(self.singleElementData, res)

    def test_comparison_unequal_different_unit(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2., ureg.kBq)))])}
        self.assertNotEqual(self.singleElementData, res)

    def test_add_element_not_existing(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0),
                                     StoredData(PQ.Activity(10., 2.),
                                                PQ.AoverLE(10., 2.)))])}
        self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append(PQ.AoverLE(10., 2.))
        self.assertEqual(self.singleElementData, res)

    def test_add_multiple_elements_not_existing(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0),
                                     StoredData(PQ.Activity(10., 2.),
                                                PQ.AoverLE(10., 2.),
                                                PQ.DoseRate(20., 3.)))])}
        self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append(PQ.AoverLE(10., 2.),
                                                                   PQ.DoseRate(20., 3.))
        self.assertEqual(self.singleElementData, res)

    def test_add_multiple_elements_not_existing_as_list(self):
        self.assertRaises(ValueError, self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append,
                          [PQ.AoverLE(10., 2.), PQ.DoseRate(20., 3.)])

    def test_add_single_element_to_existing(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0),
                                     StoredData(PQ.Activity(20., sqrt(8.))))])}
        self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append(PQ.Activity(10., 2.))
        self.assertEqual(self.singleElementData, res)

    def test_check_single_element_is_exisiting(self):
        self.assertTrue(self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].has_quantity("Activity"))

    def test_check_multiple_element_is_exisiting(self):
        self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append(PQ.AoverLE(10., 2.))
        self.assertTrue(self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].has_quantity(["Activity", "AoverLE"]))

    def test_check_single_element_not_exisiting(self):
        self.assertFalse(self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].has_quantity("AoverLE"))

    def test_check_multiple_element_not_exisiting(self):
        self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append(PQ.AoverLE(10., 2.))
        self.assertFalse(self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].has_quantity(["Activity",
                                                                                           "AoverLE",
                                                                                           "DoseRate"]))
        
    def test_operator_access(self):
        self.assertEqual(self.singleElementData["det1"][PQ.Isotope(3, 1, 0)]["Activity"],
                         PQ.Activity(10., 2.))

    def test_global_data_single_pair(self):
        _global_data.add("NoOfProtons", 10.)
        self.assertEqual(_global_data["NoOfProtons"], 10.)

    def test_global_data_nested(self):
        _global_data.add("det1", "Mass", PQ.Mass(10, ureg.kg))
        self.assertEqual(_global_data["det1"]["Mass"], PQ.Mass(10, ureg.kg))

    def test_global_data_invalid_request(self):
        self.assertRaises(KeyError, _global_data.__getitem__, "InvalidArgument")

    def test_global_data_eq_non_dict(self):
        self.assertFalse(_global_data == [])

    def test_global_data_equal_op(self):
        from collections import defaultdict
        _global_data.data = defaultdict(dict)
        _global_data.add("NoOfProtons", 10)
        _global_data.add("det1", "TotalActivity", PQ.Activity(10., 2.))
        res = {"NoOfProtons": 10, "det1": {"TotalActivity": PQ.Activity(10., 2.)}}
        self.assertEqual(_global_data, res)

    def test_named_store_constructor(self):
        inp = StoredData(PQ.Activity(10., 2.),
                         ScaledActivity=PQ.Activity(50., 2.))
        self.assertEqual(inp["ScaledActivity"], PQ.Activity(50., 2.))

    def test_named_store_add(self):
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0),
                                     StoredData(PQ.Activity(10., 2.),
                                                ScaledActivity=PQ.Activity(50., 2.)))])}
        self.singleElementData["det1"][PQ.Isotope(3, 1, 0)].append(ScaledActivity=PQ.Activity(50., 2.))
        self.assertEqual(self.singleElementData, res)

    def test_set_item(self):
        data = StoredData(PQ.Activity(10., 2.))
        data["Activity"] = PQ.Activity(20., 2.)
        res = PQ.Activity(20., 2.)
        self.assertEqual(data["Activity"], res)

    def test_access_none(self):
        data = StoredData(PQ.Activity(10., 2.))
        self.assertEqual(data["foo"], None)
