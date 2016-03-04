import unittest
from utils.Plotter import PlotConfig as PC


class testPlotConfig(unittest.TestCase):
    def setUp(self):
        pass

    def testType(self):
        x = {'type': '1D'}
        pc = PC("foo", x)
        self.assertEqual(pc.type, '1D')

    def testEquals(self):
        x = {"type" : "1D"}
        pc1 = PC("foo", x)
        pc2 = PC("bar", x)
        self.assertEqual(pc1, pc2)

