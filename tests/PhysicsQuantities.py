import unittest
import utils.PhysicsQuantities as PQ
from utils import ureg


class TestPhysicsQuantities(unittest.TestCase):
    def setUp(self):
        pass

    def testIsotopeCreationFromString(self):
        isotope = PQ.Isotope(3, "H")
        self.assertEqual([isotope.A, isotope.Z], [3, 1])

    def testIsotopeCreationFromString(self):
        isotope = PQ.Isotope(3, 1)
        self.assertEqual([isotope.A, isotope.Z], [3, 1])

    def testIsotopeException(self):
        self.assertRaises(ValueError, PQ.Isotope, [3, float(1.)])

    def testIsotopesEqualsSameCtor(self):
        isotope1 = PQ.Isotope(3, 1)
        isotope2 = PQ.Isotope(3, 1)
        self.assertEqual(isotope1, isotope2)

    def testIsotopesEqualsDifferentCtor(self):
        isotope1 = PQ.Isotope(3, 1)
        isotope2 = PQ.Isotope(3, "H")
        self.assertEqual(isotope1, isotope2)

    def testIsotopesUnEqualsSameCtorA(self):
        isotope1 = PQ.Isotope(2, 1)
        isotope2 = PQ.Isotope(3, 1)
        self.assertNotEqual(isotope1, isotope2)

    def testIsotopesEqualsDifferentCtorA(self):
        isotope1 = PQ.Isotope(2, 1)
        isotope2 = PQ.Isotope(3, "H")
        self.assertNotEqual(isotope1, isotope2)

    def testIsotopesUnEqualsSameCtorZ(self):
        isotope1 = PQ.Isotope(2, 1)
        isotope2 = PQ.Isotope(3, 7)
        self.assertNotEqual(isotope1, isotope2)

    def testIsotopesEqualsDifferentCtorZ(self):
        isotope1 = PQ.Isotope(2, 1)
        isotope2 = PQ.Isotope(3, "B")
        self.assertNotEqual(isotope1, isotope2)

    def testIsotopesUnEqualsSameCtorIso(self):
        isotope1 = PQ.Isotope(2, 1, 1)
        isotope2 = PQ.Isotope(3, 1)
        self.assertNotEqual(isotope1, isotope2)

    def testIsotopesEqualsDifferentCtorIso(self):
        isotope1 = PQ.Isotope(2, 1, 1)
        isotope2 = PQ.Isotope(3, "H")
        self.assertNotEqual(isotope1, isotope2)

    def testH10EqualsSameUnit(self):
        val1 = PQ.H10(10.)
        val2 = PQ.H10(10.)
        self.assertEqual(val1, val2)

    def testH10EqualsDiffUnit(self):
        val1 = PQ.H10(10.)
        val2 = PQ.H10(0.01, ureg.kBq / (ureg.mSv / ureg.hour))
        self.assertEqual(val1, val2)

    def testH10UnEqualsSameUnit(self):
        val1 = PQ.H10(20.)
        val2 = PQ.H10(10.)
        self.assertNotEqual(val1, val2)

    def testH10UnEqualsDiffUnit(self):
        val1 = PQ.H10(20.)
        val2 = PQ.H10(0.01, ureg.kBq / (ureg.mSv / ureg.hour))
        self.assertNotEqual(val1, val2)