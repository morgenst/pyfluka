__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
from reader.UsrbinReader import UsrbinReader as UR


class TestUsrbinReader(unittest.TestCase):
    def setUp(self):
        self.reader = UR("Activity")

    def testReadKeys(self):
        d = self.reader.load("UsrbinInputTest.ascii")
        self.assertTrue("Dose-2y" in d)
        self.assertTrue("Activity" in d["Dose-2y"])
        self.assertTrue("Binning" in d["Dose-2y"])
        self.assertTrue("Weight" in d["Dose-2y"])

