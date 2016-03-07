import unittest
import pickle
from reader import _dh


class DataHandle(unittest.TestCase):
    def setUp(self):
        fLE = open("../data/LEDB.p", "r")
        self.dLE = pickle.load(fLE)
        fLE.close()

        fH10 = open("../data/Activity_H10_conversion.p", "r")
        self.dH10 = pickle.load(fH10)
        fH10.close()

        fHp007 = open("../data/Activity_Hp007_conversion.p", "r")
        self.dHp007 = pickle.load(fHp007)
        fHp007.close()

    def testLE(self):
        self.assertEqual(_dh._LE, self.dLE)

    def testH10(self):
        self.assertEqual(_dh._H10, self.dH10)

    def testHp007(self):
        self.assertEqual(_dh._Hp007, self.dHp007)
