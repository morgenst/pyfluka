__author__ = 'marcusmorgenstern'
__mail__ = ''

import os
import unittest
from os.path import join

from pyfluka.reader.GeometryReader import GeometryReader

_basedir = os.path.dirname(__file__)


class TestGeometryReader(unittest.TestCase):
    def setUp(self):
        self.geo_file = join(_basedir, "test_data/testGeometry.ascii")
        self.reader = GeometryReader()

    def test_load(self):
        xs, ys = self.reader.load(self.geo_file)
        self.assertGreater(len(xs), 0)
        self.assertGreater(len(ys), 0)

