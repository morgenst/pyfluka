import unittest
from pyfluka.base import IllegalArgumentError
from pyfluka.reader.BaseReader import BaseReader
from pyfluka.utils import ureg


class TestBaseReader(unittest.TestCase):
    def setUp(self):
        pass

    def test_ctor_dim(self):
        reader = BaseReader("Activity", "kBq", None)
        self.assertEqual(reader.dim, ureg.kBq)

    @unittest.skip("Not implemented")
    def test_load_single_file_weight(self):
        reader = BaseReader("Activity", "kBq", [2.])
        reader.load("")

    def test_exception_invalid_files(self):
        reader = BaseReader("Activity", "kBq", [2.])
        self.assertRaises(IllegalArgumentError, reader.load, ())
