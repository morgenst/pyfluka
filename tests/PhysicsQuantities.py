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

    def test_string(self):
        val = PQ.Activity(20., 2.)
        self.assertEqual('{!s}'.format(val), "Activity: 20.0 Bq +- 2.0 Bq")

    def test_latex_no_units(self):
        val = PQ.Activity(20., 2.)
        self.assertEqual('{:Lnu}'.format(val), "$20.0 \pm 2.0 $")

    def test_latex_no_unc(self):
        val = PQ.Activity(20., 2.)
        self.assertEqual('{:Lne}'.format(val), "$20.0 Bq$")

    def test_latex_no_units_no_unc(self):
        val = PQ.Activity(20., 2.)
        self.assertEqual('{:Lnune}'.format(val), "$20.0 $")

    def test_latex_float_precision(self):
        val = PQ.Activity(20.12345678, 2.123456)
        self.assertEqual("{:.2fL}".format(val), "$20.12 Bq \pm 2.12 Bq$")

    def test_different_types_equals(self):
        q1 = PQ.Mass(100, 2)
        q2 = PQ.Mass(100., 2.)
        self.assertEqual(q1, q2)

    def test_multiplication_scalar_float_lhs(self):
        product = 5. * PQ.Activity(20., 2.)
        res = PQ.Activity(100., 2.)
        self.assertEqual(product, res)

    def test_multiplication_scalar_float_rhs(self):
        product = PQ.Activity(20., 2.) * 5.
        res = PQ.Activity(100., 2.)
        self.assertEqual(product, res)

    def test_multiplication_scalar_int_lhs(self):
        product = 5 * PQ.Activity(20., 2.)
        res = PQ.Activity(100., 2.)
        self.assertEqual(product, res)

    def test_multiplication_scalar_int_rhs(self):
        product = PQ.Activity(20., 2.) * 5
        res = PQ.Activity(100., 2.)
        self.assertEqual(product, res)

    def test_multiplication_different_pq_no_unc(self):
        product = PQ.Dose(PQ.Activity(10., 0.) * PQ.Activity(10., 0.))
        res = PQ.Activity(100., 0., ureg.Bq * ureg.Bq)
        self.assertEqual(product, res)

    def test_multiplication_different_pq_no_unc(self):
        product = PQ.Dose(PQ.Activity(10., 0.) * PQ.EInh(10.))
        res = PQ.Dose(100., -1.)
        self.assertEqual(product, res)

    def test_production_yield_create(self):
        prod_yield = PQ.ProductionYield(10., 2.)
        res = ureg.Quantity(10., 1./ureg.second)
        self.assertEqual(prod_yield.val, res)
