__author__ = 'morgenst'

import os.path
import unittest
from collections import OrderedDict
from shutil import rmtree

import pyfluka.utils.PhysicsQuantities as PQ
from pyfluka.base import InvalidInputError

from pyfluka.base.StoredData import StoredData
from pyfluka.plugins.TableMaker import Column
from pyfluka.plugins.TableMaker import TableMaker as TM
from pyfluka.utils.ShellUtils import mkdir


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

    def test_eq_operator_true(self):
        col1 = Column("foo1")
        col2 = Column("foo1")
        self.assertEqual(col1, col2)

    def test_eq_operator_false(self):
        col1 = Column("foo1")
        col2 = Column("foo2")
        self.assertNotEqual(col1, col2)
