__author__ = 'marcusmorgenstern'
__mail__ = ''

import copy
import unittest
import numpy as np
from base import InvalidInputError
from reader.UsrbinReader import UsrbinReader as UR
from utils import PhysicsQuantities as PQ
from operator import mul


class TestUsrbinReader(unittest.TestCase):
    def setUp(self):
        self.reader = UR("Activity")
        dataraw = [4.3201E-07, 1.5970E-06, 4.6090E-05, 1.5935E-06, 5.0045E-07, 8.6618E-07, 4.1063E-06, 9.8403E-05,
                   3.5158E-06, 7.2260E-07]
        dataraw = [PQ.Activity(i) for i in dataraw]
        binning = [(-45., 45., 1), (-54., 54., 5), (-33., 36., 2)]
        binning_reverse = [2, 5, 1]
        self.data_tutorial = {"EneDep2": {"Weight": (100., 100.),
                                          "Binning": binning,
                                          "Activity": np.reshape(np.array(dataraw), binning_reverse).transpose()}}

    def test_read_keys(self):
        d = self.reader.load("UsrbinInputTest.ascii")
        self.assertTrue("EneDep2" in d)
        self.assertTrue("Activity" in d["EneDep2"])
        self.assertTrue("Binning" in d["EneDep2"])
        self.assertTrue("Weight" in d["EneDep2"])

    def test_read_simple(self):
        d = self.reader.load("UsrbinInputTest.ascii")
        self.assertEqual(d["EneDep2"]["Weight"], self.data_tutorial["EneDep2"]["Weight"])
        self.assertEqual(d["EneDep2"]["Binning"], self.data_tutorial["EneDep2"]["Binning"])
        self.assertEqual(d["EneDep2"]["Activity"].all(), self.data_tutorial["EneDep2"]["Activity"].all())

    def test_read_multiple(self):
        d = self.reader.load(["UsrbinInputTest.ascii", "UsrbinInputTest.ascii"])
        self.data_tutorial["EneDep2"]["Activity"] *= 2
        self.data_tutorial["EneDep2"]["Weight"] = (200, 200)
        self.assertEqual(d["EneDep2"]["Weight"], self.data_tutorial["EneDep2"]["Weight"])
        self.assertEqual(d["EneDep2"]["Binning"], self.data_tutorial["EneDep2"]["Binning"])
        self.assertEqual(d["EneDep2"]["Activity"].all(), self.data_tutorial["EneDep2"]["Activity"].all())

    def test_validate_merging_exception_binning_merge_call(self):
        data_fail = copy.deepcopy(self.data_tutorial)
        data_fail["EneDep2"]["Binning"] = [(-45., 45., 3), (-54., 54., 5), (-33., 36., 2)]
        self.assertRaises(InvalidInputError, UR._merge, self.data_tutorial, data_fail)
