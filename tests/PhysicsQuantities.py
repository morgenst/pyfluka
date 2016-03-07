import unittest
import utils.PhysicsQuantities as PQ
from utils import ureg
from math import sqrt


class TestPhysicsQuantities(unittest.TestCase):
    def setUp(self):
        pass

    def testIsotopeCreationFromString(self):
        isotope = PQ.Isotope(3, "H")
        self.assertEqual([isotope.A, isotope.Z], [3, 1])

    def testIsotopeCreationFromInteger(self):
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
        
    def testActivityEqualsSameUnit(self):
        val1 = PQ.Activity(10.)
        val2 = PQ.Activity(10.)
        self.assertEqual(val1, val2)

    def testActivityEqualsDiffUnit(self):
        val1 = PQ.Activity(10.)
        val2 = PQ.Activity(0.01, unit=ureg.kBq)
        self.assertEqual(val1, val2)

    def testActivityUnEqualsSameUnit(self):
        val1 = PQ.Activity(20.)
        val2 = PQ.Activity(10.)
        self.assertNotEqual(val1, val2)

    def testActivityUnEqualsDiffUnit(self):
        val1 = PQ.Activity(20.)
        val2 = PQ.Activity(20., unit=ureg.kBq)
        self.assertNotEqual(val1, val2)

    def testActivityEqualsUnc(self):
        val1 = PQ.Activity(20., 2.1)
        val2 = PQ.Activity(20., 2.1)
        self.assertEqual(val1, val2)

    def testActivityUnEqualsDiffUnc(self):
        val1 = PQ.Activity(20., 2.1)
        val2 = PQ.Activity(20., 3.1)
        self.assertNotEqual(val1, val2)

    def testSummationActivityEquals(self):
        val1 = PQ.Activity(20., 2.)
        val2 = PQ.Activity(10., 3.)
        unc = sqrt(pow(2., 2) + pow(3., 2))
        res = PQ.Activity(30., unc)
        self.assertEqual(val1 + val2, res)

    @unittest.skip("Not implemented")
    def testSummationActivityDifferentUnitsEquals(self):
        val1 = PQ.Activity(20., 2.)
        val2 = PQ.Activity(10., 3.)
        unc = sqrt(pow(2., 2) + pow(3., 2))
        res = PQ.Activity(30., unc)
        self.assertEqual(val1 + val2, res)

    @unittest.skip("Not implemented")
    def testDose(self):
        pass

    def testLatexString(self):
        val = PQ.Activity(20., 2.)
        self.assertEqual('{:L}'.format(val), "$20.0 Bq \pm 2.0 Bq$")

    def testString(self):
        val = PQ.Activity(20., 2.)
        self.assertEqual('{!s}'.format(val), "Activity: 20.0 Bq +- 2.0 Bq")


