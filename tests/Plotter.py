import unittest
from utils.Plotter import Plotter
from reader.UsrbinReader import UsrbinReader as UR


class TestPlotter(unittest.TestCase):
    def setUpTestData(self):
        reader = UR("Activity")
        self.data = reader.load("UsrbinInputTest.ascii")['Dose-2y']

    def setUp(self):
        self.plotter = Plotter()
        self.setUpTestData()


    def testPlotMatrix(self):
        print len(self.data[0])
        self.plotter.plotMatrix(self.data[0], self.data[1])