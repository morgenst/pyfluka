__author__ = 'morgenst'

import unittest
from plugins.TableMaker import TableMaker as TM
from plugins.TableMaker import Column

class TableMakerTest(unittest.TestCase):
    def setUp(self):
        self.tabConfig = {"cols" : ["Isotope", "Activity"]}

    def testConfig(self):
        tm = TM(self.tabConfig)
        res = [Column(col) for col in self.tabConfig['cols']]
        self.assertEqual(tm.cols, res)
