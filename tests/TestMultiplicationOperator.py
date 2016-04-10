import unittest
from collections import OrderedDict
from base.StoredData import StoredData
from base import _global_data, IllegalArgumentError, InvalidInputError
from plugins.Multiplication import MultiplicationOperator
from utils import PhysicsQuantities as PQ
from utils import ureg


class TestMultiplicationOperator(unittest.TestCase):
    def setUp(self):
        self.dataActivity = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.)))])}
        self.dataActivityEinh = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0),
                                                       StoredData(PQ.Activity(10., 2.),
                                                                  inhalationcoeff=PQ.EInh(10.)))])}
        self.config_scalar_const = d = {"type": "scalar",
                                        "multiplier": "Activity",
                                        "multiplicand": "const:5",
                                        "product": "ScaledActivity:Activity"}
        self.config_dict_builtin = d = {"type": "dict",
                                        "multiplier": "Activity",
                                        "multiplicand": "builtin:einh",
                                        "product": "InhalationDose:Dose"}

    def test_config(self):
        mul_op = MultiplicationOperator(**self.config_scalar_const)
        self.assertTrue(mul_op.scalar)
        self.assertEqual(mul_op.multiplier, "Activity")
        self.assertEqual(mul_op.multiplicand, 5.)
        self.assertEqual(mul_op.product, "ScaledActivity")

    def test_scalar_const_multiplication(self):
        mul_op = MultiplicationOperator(**self.config_scalar_const)
        mul_op.invoke(self.dataActivity)
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.),
                                                                     ScaledActivity=PQ.Activity(50., 2.)))])}
        self.assertEqual(self.dataActivity, res)

    def test_dict_builtin_dh_multiplication(self):
        mul_op = MultiplicationOperator(**self.config_dict_builtin)
        mul_op.invoke(self.dataActivity)
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.),
                                                                     InhalationDose=PQ.Dose(10. * 4.10E-011,
                                                                                            -1., ureg.Sv)))])}
        self.assertEqual(self.dataActivity, res)

    @unittest.skip("Not implemented")
    def test_dict_multiplication_default_type(self):
        pass

    def test_dict_multiplication_stored_quantity(self):
        d = {"type": "dict",
             "multiplier": "Activity",
             "multiplicand": "inhalationcoeff",
             "product": "InhalationDose:Dose"}
        mul_op = MultiplicationOperator(**d)
        mul_op.invoke(self.dataActivityEinh)
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(10., 2.),
                                                                     inhalationcoeff=PQ.EInh(10.),
                                                                     InhalationDose=PQ.Dose(100.,
                                                                                            -1., ureg.Sv)))])}
        self.assertEqual(self.dataActivityEinh, res)

    def test_dict_multiplication_global_data(self):
        d = {"type": "scalar",
             "multiplier": "ProductionYield",
             "multiplicand": "global:NoOfPrimaries",
             "product": "Activity"}
        _global_data.add("NoOfPrimaries", 10.)
        data = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.ProductionYield(10., 0.)))])}
        mul_op = MultiplicationOperator(**d)
        mul_op.invoke(data)
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.ProductionYield(10., 0.),
                                                                     PQ.Activity(100., 0.)))])}
        self.assertEqual(data, res)

    def test_dict_multiplication_det(self):
        d = {"type": "dict",
             "multiplier": "Activity",
             "multiplicand": "global:mass",
             "product": "SpecificActivity"}
        _global_data.add("det1", "mass", PQ.Mass(10., "kg"))
        mul_op = MultiplicationOperator(**d)
        data = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.Activity(100., 0.)))])}
        mul_op.invoke(data)
        res = PQ.SpecificActivity(10.)
        self.assertEqual(data["det1"][PQ.Isotope(3, 1, 0)]["SpecificActivity"], res)

    @unittest.skip("Not implement. Supposed to check against exception")
    def test_dict_multiplication_det_non_existing(self):
        pass

    def test_find_builtin_fail(self):
        mul_op = MultiplicationOperator(**self.config_scalar_const)
        self.assertRaises(IllegalArgumentError, mul_op.find_builtin, "foo")

    def test_ctor_missing_multiplicand(self):
        config = {"type": "scalar",
                  "multiplier": "Activity",
                  "product": "ScaledActivity:Activity"}
        self.assertRaises(InvalidInputError, MultiplicationOperator, **config)

    def test_ctor_missing_multiplier(self):
        config = {"type": "scalar",
                  "multiplicand": "Activity",
                  "product": "ScaledActivity:Activity"}
        self.assertRaises(InvalidInputError, MultiplicationOperator, **config)

    def test_ctor_missing_product(self):
        config = {"type": "scalar",
                  "multiplier": "Activity",
                  "multiplicand": "Activity"}
        self.assertRaises(InvalidInputError, MultiplicationOperator, **config)

    def test_ctor_missing_type(self):
        config = {"multiplier": "Activity",
                  "multiplicand": "Activity",
                  "product": "ScaledActivity:Activity"}
        self.assertRaises(InvalidInputError, MultiplicationOperator, **config)

    def test_parsing_const_val_with_unit_simple(self):
        config = {"type": "scalar",
                  "multiplier": "DoseRate",
                  "multiplicand": "const:100 hour",
                  "product": "Dose"}
        mul_op = MultiplicationOperator(**config)
        self.assertEqual(mul_op.multiplicand, PQ.Time(100, unit=ureg.hour))

    def test_custom_product_type(self):
        config = {"type": "scalar",
                  "multiplier": "DoseRate",
                  "multiplicand": "const:100 hour",
                  "product": "MyCustomDose"}
        mul_op = MultiplicationOperator(**config)
        self.assertEqual(mul_op.quantity(100, unit=ureg.Sv), PQ.Dose(100))
