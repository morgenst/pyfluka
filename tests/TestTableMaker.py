__author__ = 'morgenst'

import unittest
import os.path
import utils.PhysicsQuantities as PQ
from base import InvalidInputError
from base.StoredData import StoredData
from collections import OrderedDict
from plugins.TableMaker import TableMaker as TM
from plugins.TableMaker import Column
from utils.ShellUtils import mkdir
from shutil import rmtree


class TableMakerTest(unittest.TestCase):
    def setUp(self):
        self.tabConfig = {"cols": ["Isotope", "Activity"]}
        self.data = {"det1": OrderedDict([(PQ.Isotope(3, "H"), StoredData(PQ.Activity(10.00101010101)))])}
        self.dataMultiDet = {"det1": OrderedDict([(PQ.Isotope(3, "H"), StoredData(PQ.Activity(10.00101010101)))]),
                             "det2": OrderedDict([(PQ.Isotope(3, "H"), StoredData(PQ.Activity(100.00101010101)))])}
        self.tm = TM(self.tabConfig)

    @classmethod
    def tearDownClass(cls):
        os.remove("tables.tex")
        os.remove("table_det1.tex")
        os.remove("table_det2.tex")
        rmtree("test_table_maker")

    def testConfig(self):
        tm = TM(self.tabConfig)
        res = [Column(col) for col in self.tabConfig['cols']]
        self.assertEqual(tm.cols, self.tabConfig['cols'])

    def testInvoke(self):
        self.tm.invoke(self.data)

    def testMultipleDetectors(self):
        self.tm.cols = self.tabConfig["cols"]
        self.tm.invoke(self.dataMultiDet)
        self.assertEqual(self.dataMultiDet.keys(), self.tm.tables.keys())

    def testDumpSingleFile(self):
        self.tm.invoke(self.data)
        self.assertTrue(os.path.exists("tables.tex"))

    def testDumpMultipleFiles(self):
        tabConfig = {"cols": ["Isotope", "Activity"], "multipleOutputFiles": True}
        tm = TM(tabConfig)
        tm.invoke(self.dataMultiDet)
        self.assertTrue(os.path.exists("table_det1.tex"))
        self.assertTrue(os.path.exists("table_det2.tex"))

    def testDumpCustomOutPathSingleFile(self):
        mkdir("test_table_maker")
        tabConfig = {"cols": ["Isotope", "Activity"], "outputdir": "test_table_maker"}
        tm = TM(tabConfig)
        tm.invoke(self.data)
        self.assertTrue(os.path.exists("test_table_maker/tables.tex"))

    @unittest.skip("Not implemented")
    def testHeader(self):
        pass

    def testNoColDefinitionException(self):
        self.assertRaises(InvalidInputError, TM, {})

    def testNonExistingOutDirException(self):
        tabConfig = {"cols": ["Isotope", "Activity"], "outputdir": "non_existing_dir"}
        self.assertRaises(ValueError, TM, tabConfig)

