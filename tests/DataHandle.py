import unittest
import pickle
from reader import _dh


class TestDataHandle(unittest.TestCase):
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

        f_einh = open("../data/inhalation.p", "r")
        self.d_einh = pickle.load(f_einh)
        f_einh.close()

        f_eing = open("../data/ingestion.p", "r")
        self.d_eing = pickle.load(f_eing)
        f_eing.close()

    def testLE(self):
        self.assertEqual(_dh._le, self.dLE)

    def testH10(self):
        self.assertEqual(_dh._h10, self.dH10)

    def testHp007(self):
        self.assertEqual(_dh._hp007, self.dHp007)

    def test_einh(self):
        self.assertEqual(_dh._einh, self.d_einh)

    def test_eing(self):
        self.assertEqual(_dh._eing, self.d_eing)