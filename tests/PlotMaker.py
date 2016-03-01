import unittest
import numpy as np
from utils import PhysicsQuantities as PQ
from utils.Plotter import PlotConfig as PC
from plugins.PlotMaker import PlotMaker as PM
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison


class PlotMaker(unittest.TestCase):
    def setUp(self):
        self.plotConfig = [PC({'type': "2D", 'quantity': "Activity"})]
        self.pm = PM(self.plotConfig)
        rawDataArr = np.array([PQ.Activity(i) for i in range(1000)])
        self.rawData = {"Det1": {'Activity': (rawDataArr, [(0, 1, 1), (0, 100, 20), (0, 150, 50)])}}

        self.data = np.reshape(rawDataArr,[20,50,1]).transpose()
        self.refPlot = plt.pcolor(self.data[0].astype(float))

    #@image_comparison(baseline_images=['self.refPlot'])
    @unittest.skip("not fully implemented yet")
    def testPlotMatrix(self):
        plot = self.pm.invoke(self.rawData)
        plot.show()

    def testAddPlotConfig(self):
        self.assertItemsEqual(self.pm.config, self.plotConfig)

    def testPlot2DSimpleHasKey(self):
        self.pm.invoke(self.rawData)
        p = self.pm.plots
        self.assertTrue(p.has_key('2D'))

    def testInvalidPlotConfigWrongQuantity(self):
        plotConfigInvalid = [PC({"type": "2D"})]
        pm = PM(plotConfigInvalid)
        self.assertRaises(AttributeError, pm.invoke, self.rawData)
