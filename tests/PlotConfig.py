import unittest
from utils.Plotter import PlotConfig as PC


class testPlotConfig(unittest.TestCase):
    def setUp(self):
        pass

    def testType(self):
        x = {'type': '1D'}
        pc = PC(x)
        self.assertEqual(pc.type, '1D')

    def testEqulas(self):
        x = {"type" : "1D"}
        pc1 = PC(x)
        pc2 = PC(x)
        self.assertEqual(pc1, pc2)