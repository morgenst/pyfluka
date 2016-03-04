__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
from reader.UsrbinReader import UsrbinReader as UR

class TestUsrbinReader(unittest.TestCase):
    def setUp(self):
        self.reader = UR("Activity")

    def testReadKeys(self):
        d = self.reader.load("UsrbinInputTest.ascii")
        self.assertTrue(d.has_key("Dose-2y"))
        self.assertTrue(d["Dose-2y"].has_key("Activity"))
        self.assertTrue(d["Dose-2y"].has_key("Binning"))
        self.assertTrue(d["Dose-2y"].has_key("Weight"))
