import unittest
from collections import OrderedDict
from base.StoredData import StoredData
from base import _global_data
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
        d = {"type": "dict",
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
