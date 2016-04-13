import os
import pickle
import unittest
from os.path import join

from pyfluka.utils import ureg

from pyfluka.reader import _dh
from pyfluka.utils import PhysicsQuantities as PQ

_basedir = os.path.dirname(__file__)


class TestDataHandle(unittest.TestCase):
    def setUp(self):
        fLE = open(join(_basedir, "../pyfluka/data/LEDB.p"), "r")
        self.dLE = pickle.load(fLE)
        fLE.close()

        fH10 = open(join(_basedir, "../pyfluka/data/Activity_H10_conversion.p"), "r")
        self.dH10 = pickle.load(fH10)
        fH10.close()

        fHp007 = open(join(_basedir, "../pyfluka/data/Activity_Hp007_conversion.p"), "r")
        self.dHp007 = pickle.load(fHp007)
        fHp007.close()

        f_einh = open(join(_basedir, "../pyfluka/data/inhalation.p"), "r")
        self.d_einh = pickle.load(f_einh)
        f_einh.close()

        f_eing = open(join(_basedir, "../pyfluka/data/ingestion.p"), "r")
        self.d_eing = pickle.load(f_eing)
        f_eing.close()

        f_hl = open(join(_basedir, "../pyfluka/data/half_lifes.p"), "r")
        self.d_hl = pickle.load(f_hl)
        f_hl.close()

        self.test_isotopes = [PQ.Isotope(3, 1), PQ.Isotope(60, "Co"), PQ.Isotope(40, "K"), PQ.Isotope(137, "Cs")]

    def test_le(self):
        self.assertEqual(_dh._le, self.dLE)

    def test_h10(self):
        self.assertEqual(_dh._h10, self.dH10)

    def testHp007(self):
        self.assertEqual(_dh._hp007, self.dHp007)

    def test_einh(self):
        self.assertEqual(_dh._einh, self.d_einh)

    def test_eing(self):
        self.assertEqual(_dh._eing, self.d_eing)

    def test_hl(self):
        self.assertEqual(_dh._hl, self.d_hl)

    def test_hl_isotopes(self):
        res = [PQ.Time(12.33, 0., ureg.year),
               PQ.Time(5.271, 0., ureg.year),
               PQ.Time(1.265e+09, 0., ureg.year),
               PQ.Time(30.04, 0., ureg.year)]
        values = [_dh._hl[isotope] for isotope in self.test_isotopes]
        self.assertEqual(values, res)
