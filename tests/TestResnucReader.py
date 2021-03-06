import os
import unittest
from collections import OrderedDict
from os.path import join

from numpy import sqrt

import pyfluka.utils.PhysicsQuantities as PQ
from pyfluka.base.StoredData import StoredData
from pyfluka.reader.ResnucReader import ResnucReader as RR

_basedir = os.path.dirname(__file__)


class TestResnucReader(unittest.TestCase):
    def setUp(self):
        self.reader = RR()
        self.maxDiff = None

    def testTabLisRead(self):
        res = {"AlBa-1s": OrderedDict([(PQ.Isotope(75, 32, 0),
                                        StoredData(PQ.Activity(2.0663E+05, unc=0.99 * 2.0663E+05))),
                                       (PQ.Isotope(26, 13, 1),
                                        StoredData(PQ.Activity(2.2300E+10, unc=0.001845 * 2.2300E+10)))])}
        data = self.reader.load(join(_basedir, "test_data/ResnucInputTest_tab.lis"))
        self.assertEqual(data, res)

    def test_tablis_read_multi_det(self):
        res = {"AlBa-1s": OrderedDict([(PQ.Isotope(75, 32, 0),
                                        StoredData(PQ.Activity(2.0663E+05, unc=0.99 * 2.0663E+05))),
                                       (PQ.Isotope(26, 13, 1),
                                        StoredData(PQ.Activity(2.2300E+10, unc=0.001845 * 2.2300E+10)))]),
               "AlBa-1y": OrderedDict([(PQ.Isotope(75, 32, 0),
                                        StoredData(PQ.Activity(2.0663E+05, unc=0.99 * 2.0663E+05))),
                                       (PQ.Isotope(26, 13, 1),
                                        StoredData(PQ.Activity(2.2300E+10, unc=0.001845 * 2.2300E+10)))])}

        data = self.reader.load(join(_basedir, "test_data/ResnucInputTestMultiDet_tab.lis"))
        self.assertEqual(data, res)

    def testMultiFileReadSingleDet(self):
        data = self.reader.load([join(_basedir, "test_data/ResnucInputTest_tab.lis"),
                                 join(_basedir, "test_data/ResnucInputTest_tab.lis")])
        res = {"AlBa-1s": OrderedDict([(PQ.Isotope(75, 32, 0),
                                        StoredData(PQ.Activity(2. * 2.0663E+05, unc=0.99 * sqrt(2.) * 2.0663E+05))),
                                       (PQ.Isotope(26, 13, 1),
                                        StoredData(PQ.Activity(2. * 2.2300E+10,
                                                               unc=0.001845 * sqrt(2.) * 2.2300E+10)))])}
        self.assertEqual(data, res)

    @unittest.skip("To be implemented")
    def testMultiFileReadMultiDet(self):
        data = self.reader.load(["test_data/ResnucInputTest_tab.lis", "test_data/ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc=0.99 * 2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc=0.001845 * 2.2300E+10)]}}
        self.assertFalse(True, "To be implemented")

    def test_multi_file_read_weighted(self):
        sf = 1.5
        self.reader.weights = [0.8, 0.7]
        data = self.reader.load([join(_basedir, "test_data/ResnucInputTest_tab.lis"),
                                 join(_basedir, "test_data/ResnucInputTest_tab.lis")])
        res = {"AlBa-1s": OrderedDict([(PQ.Isotope(75, 32, 0),
                                        StoredData(PQ.Activity(sf * 2.0663E+05, unc= sqrt(pow(0.8, 2) + pow(0.7, 2)) *
                                                                                          0.99 * 2.0663E+05))),
                                       (PQ.Isotope(26, 13, 1),
                                        StoredData(PQ.Activity(sf * 2.2300E+10,
                                                               unc=sqrt(pow(0.8, 2) + pow(0.7, 2)) *
                                                                   0.001845 * 2.2300E+10)))])}
        self.assertAlmostEqual(data["AlBa-1s"][PQ.Isotope(26, 13, 1)]["Activity"],
                               res["AlBa-1s"][PQ.Isotope(26, 13, 1)]["Activity"])
        self.assertAlmostEqual(data["AlBa-1s"][PQ.Isotope(75, 32, 0)]["Activity"],
                               res["AlBa-1s"][PQ.Isotope(75, 32, 0)]["Activity"])

    @unittest.skip("To be implemented")
    def testMultiFileReadMultiDetWeighted(self):
        data = self.reader.load(["test_data/ResnucInputTest_tab.lis", "test_data/ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc=0.99 * 2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc=0.001845 * 2.2300E+10)]}}
        self.assertFalse(True, "To be implemented")

    @unittest.skip("To be implemented")
    def test_multi_file_merge_diff_isotopes(self):
        data = self.reader.load(["test_data/ResnucInputTest_tab.lis", "test_data/ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(-1, -1, -1),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc=0.99 * 2.0663E+05),
                                        PQ.Activity(-1, unc= -1),
                                        PQ.Activity(2.2300E+10, unc=0.001845 * 2.2300E+10)]}}
        self.assertEqual(data, res)

    def test_tab_lis_read_custom(self):
        reader = RR(quantity="DoseRate")
        res = {"AlBa-1s": OrderedDict([(PQ.Isotope(75, 32, 0),
                                        StoredData(PQ.DoseRate(2.0663E+05, unc=0.99 * 2.0663E+05))),
                                       (PQ.Isotope(26, 13, 1),
                                        StoredData(PQ.DoseRate(2.2300E+10, unc=0.001845 * 2.2300E+10)))])}
        data = reader.load(join(_basedir, join(_basedir, "test_data/ResnucInputTest_tab.lis")))
        self.assertEqual(data, res)
