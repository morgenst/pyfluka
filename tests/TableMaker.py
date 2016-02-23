__author__ = 'morgenst'

import unittest
from plugins.TableMaker import TableMaker as TM
from plugins.TableMaker import Column
import utils.PhysicsQuantities as PQ


class TableMakerTest(unittest.TestCase):
    def setUp(self):
        self.tabConfig = {"cols" : ["Isotope", "Activity"]}
        self.data = {"Isotope" : [PQ.Isotope(3, "H")], "Activity" : [PQ.Activity(10.00101010101)]}
        self.tm = TM(self.tabConfig)

    def testConfig(self):
        tm = TM(self.tabConfig)
        res = [Column(col) for col in self.tabConfig['cols']]
        self.assertEqual(tm.cols, self.tabConfig['cols'])

    def testInvoke(self):
        self.tm.invoke(self.data)
