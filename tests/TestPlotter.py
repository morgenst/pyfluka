import os
import unittest
from os.path import join

import numpy as np

from pyfluka.reader import GeometryReader as GR
from pyfluka.utils.Plotter import Plotter

_basedir = os.path.dirname(__file__)


class TestPlotter(unittest.TestCase):
    def setUpTestData(self):
        self.rawdata = np.array([i for i in range(20) for j in range(30)])
        self.data = np.reshape(self.rawdata, [30, 20]).transpose()
        self.binning = ([0, 10, 1], [0, 20, 20], [0, 30, 30])

    def setUp(self):
        self.plotter = Plotter()
        self.setUpTestData()

    @unittest.skip("Not working on travis")
    def testPlotMatrix(self):
        p = self.plotter.plot_matrix(self.data, self.binning)
        self.assertNotEqual(p, None)

    @unittest.skip("Not working on travis")
    def test_plot_matrix_and_geometry(self):
        geometry = GR().load(join(_basedir, "test_data/testGeometry.ascii"))
        p = self.plotter.plot_matrix(self.data, self.binning, geometry_data=geometry, out_filename="foo.png")
        self.assertNotEqual(p, None)

    @unittest.skip("Not implemented")
    def testGetAxisRangeIntStep(self):
        pass

    @unittest.skip("Not implemented")
    def testGetAxisRangeFloatStep(self):
        pass
