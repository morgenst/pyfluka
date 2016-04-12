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

    def test_config(self):
        tm = TM(self.tabConfig)
        res = [Column(col) for col in self.tabConfig['cols']]
        self.assertEqual(tm.cols, self.tabConfig['cols'])

    def test_invoke(self):
        self.tm.invoke(self.data)

    def test_multiple_detectors(self):
        self.tm.cols = self.tabConfig["cols"]
        self.tm.invoke(self.dataMultiDet)
        self.assertEqual(self.dataMultiDet.keys(), self.tm.tables.keys())

    def test_dump_single_file(self):
        self.tm.invoke(self.data)
        self.assertTrue(os.path.exists("tables.tex"))

    def test_dump_multiple_files(self):
        tab_config = {"cols": ["Isotope", "Activity"], "multipleOutputFiles": True}
        tm = TM(tab_config)
        tm.invoke(self.dataMultiDet)
        self.assertTrue(os.path.exists("table_det1.tex"))
        self.assertTrue(os.path.exists("table_det2.tex"))

    def test_dump_custom_out_path_single_file(self):
        mkdir("test_table_maker")
        tab_config = {"cols": ["Isotope", "Activity"], "outputdir": "test_table_maker"}
        tm = TM(tab_config)
        tm.invoke(self.data)
        self.assertTrue(os.path.exists("test_table_maker/tables.tex"))

    def test_header_auto(self):
        tab_config = {"cols": ["Isotope", "Activity"]}
        tm = TM(tab_config)
        tm.invoke(self.data)
        table = tm.tables["det1"]
        header = "Isotope   & A [$Bq$]    \\"
        self.assertEqual(table.count(header), 1)

    def test_no_column_definition_exception(self):
        self.assertRaises(InvalidInputError, TM, {})

    def test_non_existing_out_dir_exception(self):
        tab_config = {"cols": ["Isotope", "Activity"], "outputdir": "non_existing_dir"}
        self.assertRaises(ValueError, TM, tab_config)

