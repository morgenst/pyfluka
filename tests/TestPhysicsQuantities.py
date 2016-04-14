import unittest
from math import sqrt

from pyfluka.utils import ureg

import pyfluka.utils.PhysicsQuantities as PQ
from pyfluka.base import IllegalArgumentError


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

    def test_activity_equals_diff_unit(self):
        val1 = PQ.Activity(10.)
        val2 = PQ.Activity(0.01, unit=ureg.kBq)
        self.assertEqual(val1, val2)

    def test_activity_equals_diff_unit_2(self):
        val1 = PQ.SpecificActivity(10.)
        val2 = PQ.SpecificActivity(0.01, unit=ureg.kBq/ureg.kg)
        self.assertEqual(val1, val2)

    def test_activity_equals_diff_unit_3(self):
        val1 = PQ.SpecificActivity(10., unit=ureg.Bq /ureg.g)
        val2 = PQ.SpecificActivity(10., unit=ureg.kBq / ureg.kg)
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

    def test_multiplication_different_pq_no_unc_builtin(self):
        product = PQ.Dose(PQ.Activity(10., 0.) * PQ.EInh(10.))
        res = PQ.Dose(100., -1.)
        self.assertEqual(product, res)

    def test_production_yield_create(self):
        prod_yield = PQ.ProductionYield(10., 2.)
        res = ureg.Quantity(10., 1./ureg.second)
        self.assertEqual(prod_yield.val, res)

    def test_division_scalar_float_lhs(self):
        activity = PQ.Activity(10., 2.)
        result = 5. / activity
        self.assertEqual(result, PQ.create_generic("InvertedActivity", 0.5, 0., 1. / ureg.Bq))

    def test_division_scalar_float_rhs(self):
        activity = PQ.Activity(10., 2.)
        activity /= 5.
        self.assertEqual(activity, PQ.Activity(2., 2.))

    def test_division_scalar_int_lhs(self):
        activity = PQ.Activity(10., 2.)
        result = 5 / activity
        self.assertEqual(result, PQ.create_generic("InvertedActivity", 0.5, 0., 1. / ureg.Bq))

    def test_division_scalar_int_rhs(self):
        activity = PQ.Activity(10., 2.)
        activity /= 5
        self.assertEqual(activity, PQ.Activity(2., 2.))

    def test_division_pq(self):
        activity = PQ.Activity(10., 2.)
        mass = PQ.Mass(5.)
        specific_activity = activity / mass
        self.assertEqual(specific_activity, PQ.SpecificActivity(2., 0.))

    def test_generic_pq(self):
        generic_quantity = PQ.create_generic("foo", 10., 2., ureg.Bq)
        self.assertEqual(generic_quantity.__class__.__name__, "foo")
        self.assertEqual(generic_quantity.val, ureg.Quantity(10., ureg.Bq))
        self.assertEqual(generic_quantity.unc, ureg.Quantity(2., ureg.Bq))

    def test_generic_multiplication(self):
        generic_quantity = PQ.create_generic("foo", 10., 2., ureg.Bq)
        new_value = generic_quantity * 5.
        self.assertTrue(new_value.val, ureg.Quantity(50., ureg.Bq))

    def test_generic_comparison(self):
        generic = PQ.create_generic("foo", 10., 2., ureg.Bq)
        activity = PQ.Activity(10., 2., ureg.Bq)
        self.assertEqual(generic, activity)

    def test_generic_comparison_2(self):
        generic = PQ.create_generic("foo", 10000., 2000., ureg.Bq / ureg.kg)
        res = PQ.SpecificActivity(10., 2., ureg.Bq / ureg.g)
        self.assertEqual(generic, res)

    def test_copy_ctor_generic(self):
        generic = PQ.create_generic("foo", 10000., 2000., ureg.Bq / ureg.kg)
        res = PQ.SpecificActivity(10., 2., ureg.Bq / ureg.g)
        val = PQ.SpecificActivity(generic)
        self.assertEqual(val, res)

    def test_add(self):
        self.assertEqual(PQ.Activity(25.), PQ.Activity(10.) + PQ.Activity(15.))

    def test_add_null(self):
        """
        required special case for 0 as required by sum
        """
        result = PQ.Activity(10.) + 0.
        self.assertEqual(result, PQ.Activity(10.))

    def test_radd_null(self):
        result = 0. + PQ.Activity(10.)
        self.assertEqual(result, PQ.Activity(10.))

    def test_add_different_types_number(self):
        self.assertRaises(IllegalArgumentError, lambda: PQ.Activity(10.) + 1.)

    def test_radd_different_types_number(self):
        self.assertRaises(IllegalArgumentError, lambda: 1. + PQ.Activity(10.))

    def test_add_different_types_pq(self):
        self.assertRaises(IllegalArgumentError, lambda: PQ.Activity(10.) + PQ.Dose(10.))

    def test_sub_pos(self):
        self.assertEqual(PQ.Activity(5.), PQ.Activity(15.) - PQ.Activity(10.))

    def test_sub_neg(self):
        self.assertEqual(PQ.Activity(-5.), PQ.Activity(10.) - PQ.Activity(15.))

    def test_sub_null(self):
        """
        required special case for 0 as required by sum
        """
        result = PQ.Activity(10.) - 0.
        self.assertEqual(result, PQ.Activity(10.))

    def test_rsub_null(self):
        result = 0. - PQ.Activity(10.)
        self.assertEqual(result, PQ.Activity(10.))

    def test_sub_different_types_number(self):
        self.assertRaises(IllegalArgumentError, lambda: PQ.Activity(10.) - 1.)

    def test_rsub_different_types_number(self):
        self.assertRaises(IllegalArgumentError, lambda: 1. - PQ.Activity(10.))

    def test_sub_different_types_pq(self):
        self.assertRaises(IllegalArgumentError, lambda: PQ.Activity(10.) - PQ.Dose(10.))

    def test_abs_pos(self):
        q = PQ.Activity(10.)
        qa = abs(q)
        self.assertEqual(q, qa)

    def test_abs_neg(self):
        qa = abs(PQ.Activity(-10.))
        self.assertEqual(qa, PQ.Activity(10.))

    def test_generic_formatting_latex(self):
        q = PQ.create_generic("generic", 100., 0., ureg.Bq)
        self.assertEqual("$100.0 Bq \pm 0.0 Bq$", '{:L}'.format(q))

    def test_generic_formatting_latex_nounit(self):
        q = PQ.create_generic("generic", 100., 0., ureg.Bq)
        self.assertEqual("$100.0 \pm 0.0 $", '{:Lnu}'.format(q))

    def test_get_header_activity(self):
        q = PQ.Activity(1.)
        self.assertEqual('{:Lsu}'.format(q), "A [$Bq$]")

    def test_get_header_specific_activity(self):
        q = PQ.SpecificActivity(1.)
        self.assertEqual('{:Lsu}'.format(q), "A [$\\frac{Bq}{kilogram}$]")

    def test_get_header_generic(self):
        q = PQ.create_generic("gen", 100., unit=ureg.Bq)
        self.assertEqual('{:Lsu}'.format(q), " [$Bq$]")

    def test_symbol_after_scalar_multiplication(self):
        q = PQ.SpecificActivity(100., 0., ureg.Bq)
        q *= 5
        self.assertEqual(q._symbol, "A")
