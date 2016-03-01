__author__ = 'marcusmorgenstern'
__mail__ = ''

import unittest
from reader.UsrbinReader import UsrbinReader as UR

class TestUsrbinReader(unittest.TestCase):
    def setUp(self):
        self.reader = UR("Activity")

    def testRead(self):
        d = self.reader.load("UsrbinInputTest.ascii")
        print d['Dose-2y'][0]
        print len(d['Dose-2y'][0][0])
        #print d
