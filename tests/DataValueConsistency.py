import unittest
import pickle
import utils.PhysicsQuantities as PQ


class DataTest(unittest.TestCase):
    def setUp(self):
        fH10 = open("../data/Activity_H10_conversion.p", "r")
        self.H10 = pickle.load(fH10)
        fH10.close()

        fHp007 = open("../data/Activity_Hp007_conversion.p", "r")
        self.Hp007 = pickle.load(fHp007)
        fHp007.close()

        fLE = open("../data/LEDB.p", "r")
        self.LE = pickle.load(fLE)
        fLE.close()

        self.isotopeList = [PQ.Isotope(3, "H"), PQ.Isotope(44, "Sc", 1), PQ.Isotope(46, "Sc")]
        self.H10Vals = [PQ.H10(1.000000E+12), PQ.H10(2.222222E+10), PQ.H10(3.344482E+09)]
        self.Hp007Vals = [PQ.Hp007(1.000000E+09), PQ.Hp007(5.000000E+06), PQ.Hp007(1.000000E+06)]
        self.LEVals = [PQ.ExcemptionLimit(2.00E+005), PQ.ExcemptionLimit(4.00E+003), PQ.ExcemptionLimit(7.00E+003)]

    def testH10(self):
        tmp = [self.H10[isotope] for isotope in self.isotopeList]
        self.assertEqual(tmp, self.H10Vals)

    def testHp007(self):
        tmp = [self.Hp007[isotope] for isotope in self.isotopeList]
        self.assertEqual(tmp, self.Hp007Vals)

    def testLE(self):
        tmp = [self.LE[isotope] for isotope in self.isotopeList]
        self.assertEqual(tmp, self.LEVals)
