import unittest
import numpy as np
from matplotlib import pyplot as plt
from utils.Plotter import Plotter


class TestPlotter(unittest.TestCase):
    def setUpTestData(self):
        self.rawdata = np.array([i for i in range(20) for j in range(30)])
        self.data = np.reshape(self.rawdata, [30, 20]).transpose()
        self.binning = ([0, 10, 1], [0, 20, 20],  [0, 30, 30])

    def setUp(self):
        self.plotter = Plotter()
        self.setUpTestData()

    def testPlotMatrix(self):
        p = self.plotter.plotMatrix(self.data, self.binning)
        self.assertNotEqual(p, None)

    @unittest.skip("Not implemented")
    def testGetAxisRangeIntStep(self):
        pass

    @unittest.skip("Not implemented")
    def testGetAxisRangeFloatStep(self):
        pass