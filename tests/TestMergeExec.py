import unittest
import os
import shutil
from pyfluka.pyfluka_merge import InputParser, Merger


class TestInputParser(unittest.TestCase):
    def setUp(self):
        self.parser = InputParser("test-merging")

    @classmethod
    def setUpClass(cls):
        def touch(file_name):
            f = os.path.join("test-merging", file_name)
            with open(f, 'a'):
                os.utime(f, None)
        try:
            os.mkdir("test-merging")
            touch("usrbin1.fort.10")
            touch("usrbin2.fort.11")
            touch("resnuc1.fort.12")
            touch("resnuc2.fort.13")
            touch("resnuc3.fort.13")
        except OSError:
            pass
        try:
            shutil.rmtree("test-merging-empty", ignore_errors=True)
        except OSError:
            pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("test-merging")

    def test_argument_parsing(self):
        self.assertEqual(self.parser.path, "test-merging")
        self.assertEqual(self.parser.parsedInfo, {'resnuc': [], 'usrbin': []})

    def test_get_bins(self):
        self.parser._get_bins()
        self.assertEqual(self.parser.bins, set([10, 11, 12, 13]))

    def test_drop_bin(self):
        self.parser._get_bins()
        self.assertTrue(self.parser._drop_bin(10))
        self.assertEqual(self.parser.bins, set([11,12,13]))

    def test_drop_bin_miss(self):
        self.parser._get_bins()
        self.assertFalse(self.parser._drop_bin(15))
        self.assertEqual(self.parser.bins, set([10, 11, 12, 13]))


class TestMerger(unittest.TestCase):
    def setUp(self):
        pass


