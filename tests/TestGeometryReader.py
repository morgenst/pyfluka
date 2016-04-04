__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
from reader.GeometryReader import GeometryReader


class TestGeometryReader(unittest.TestCase):
    def setUp(self):
        self.geo_file = "test_data/testGeometry.ascii"
        self.reader = GeometryReader()

    def test_load(self):
        xs, ys = self.reader.load(self.geo_file)
        self.assertGreater(len(xs), 0)
        self.assertGreater(len(ys), 0)

