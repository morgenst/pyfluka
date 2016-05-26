import os
import unittest

import numpy as np
from pyfluka.utils import PhysicsQuantities as PQ

from pyfluka.plugins.PlotMaker import PlotMaker as PM
from pyfluka.utils.Plotter import PlotConfig as PC


class TestPlotMaker(unittest.TestCase):
    def setUp(self):
        plotConfigDict = {'type': "2D", 'quantity': "Activity"}
        self.plotConfig = [PC("foo", plotConfigDict)]
        self.pm = PM([plotConfigDict], "foo")
        rawDataArr = np.array([PQ.Activity(i) for i in range(1000)])
        self.rawData = {"Det1": {'Activity': rawDataArr, "Binning": [(0, 1, 1), (0, 100, 20), (0, 150, 50)]}}

        self.data = np.reshape(rawDataArr, [20, 50, 1]).transpose()
        #self.refPlot = plt.pcolor(self.data[0].astype(float))

    #@classmethod
    #def tearDownClass(cls):
        #os.remove("fooDet1")

    # @image_comparison(baseline_images=['self.refPlot'])
    @unittest.skip("not fully implemented yet")
    def testPlotMatrix(self):
        plot = self.pm.invoke(self.rawData)
        plot.show()

    def testAddPlotConfig(self):
        self.assertEqual(self.pm.config, self.plotConfig)


    @unittest.skip("not running on travis")
    def testPlot2DSimpleHasKey(self):
        self.pm.invoke(self.rawData)
        self.assertTrue(os.path.exists("fooDet1"))


    @unittest.skip("not running on travis")
    def testInvalidPlotConfigWrongQuantity(self):
        plotConfigInvalid = [{"type": "2D"}]
        pm = PM(plotConfigInvalid)
        self.assertRaises(AttributeError, pm.invoke, self.rawData)
