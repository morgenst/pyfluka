__author__ = 'morgenst'

import unittest
import os.path
from plugins.TableMaker import TableMaker as TM
from plugins.TableMaker import Column
import utils.PhysicsQuantities as PQ


class TableMakerTest(unittest.TestCase):
    def setUp(self):
        self.tabConfig = {"cols" : ["Isotope", "Activity"]}
        self.data = {"det1": {"Isotope" : [PQ.Isotope(3, "H")], "Activity" : [PQ.Activity(10.00101010101)]}}
        self.dataMultiDet = {"det1": {"Isotope" : [PQ.Isotope(3, "H")], "Activity" : [PQ.Activity(10.00101010101)]},
                             "det2": {"Isotope" : [PQ.Isotope(3, "H")], "Activity" : [PQ.Activity(100.00101010101)]}}
        self.tm = TM(self.tabConfig)

    @classmethod
    def tearDownClass(cls):
        os.remove("tables.tex")

    def testConfig(self):
        tm = TM(self.tabConfig)
        res = [Column(col) for col in self.tabConfig['cols']]
        self.assertEqual(tm.cols, self.tabConfig['cols'])

    def testInvoke(self):
        self.tm.invoke(self.data)

    def testMultipleDetectors(self):
        self.tm.invoke(self.dataMultiDet)
        self.assertEqual(self.dataMultiDet.keys(), self.tm.tables.keys())

    def testDumpSingleFile(self):
        self.tm.invoke(self.data)
        self.assertTrue(os.path.exists("tables.tex"))