import unittest
from math import sqrt

from pyfluka.base import _global_data
from pyfluka.plugins.SimpleCalculator import *
from pyfluka.base.StoredData import StoredData
from pyfluka.utils import ureg


class TestCalculator(unittest.TestCase):
    def setUp(self):
        _global_data.add("det1", "Mass", PQ.Mass(10, ureg.kg))
        self.dataIsotopeSpecificAct = {"det1": OrderedDict([(PQ.Isotope(3, 1),
                                                             StoredData(PQ.SpecificActivity(10.)))])}
        self.dataIsotopeAct = {"det1": OrderedDict([(PQ.Isotope(3, 1),
                                                     StoredData(PQ.Activity(10.)))])}
        self.dataIsotopeMultiAct = {"det1": OrderedDict([(PQ.Isotope(3, 1),
                                                          StoredData(PQ.Activity(10.))),
                                                         (PQ.Isotope(2, 1),
                                                          StoredData(PQ.Activity(30.)))])}

        self.AoverLECalculator = AoverLECalculator()

    def test_consistency_check_pass(self):
        self.AoverLECalculator._check_consistency(self.dataIsotopeSpecificAct["det1"][PQ.Isotope(3, 1)],
                                                  ["SpecificActivity"])

    def testAoverLESimple(self):
        self.AoverLECalculator.invoke(self.dataIsotopeSpecificAct)
        self.assertEqual(self.dataIsotopeSpecificAct["det1"][PQ.Isotope(3, 1)]["AoverLE"],
                         PQ.AoverLE(10. / 2.00E+005))

    @unittest.skip("Not implemented")
    def testAoverLENonExistingLimit(self):
        pass

    def test_AoverLE_wrong_input(self):
        self.assertRaises(ValueError, self.AoverLECalculator.invoke,
                          {"det1": OrderedDict([(PQ.Isotope(3, 1), StoredData(PQ.Activity(1.)))])})

    def testSpecificActivitySimple(self):
        calculator = SpecificActivityCalculator()
        calculator.invoke(self.dataIsotopeAct)
        self.assertEqual(self.dataIsotopeAct["det1"][PQ.Isotope(3, 1)]["SpecificActivity"],
                         PQ.SpecificActivity(1.))

    def testSpecificActivitySimpleDiffMassUnit(self):
        _global_data["det1"]["Mass"] = PQ.Mass(10., ureg.g)
        calculator = SpecificActivityCalculator()
        calculator.invoke(self.dataIsotopeAct)
        self.assertEqual(self.dataIsotopeAct["det1"][PQ.Isotope(3, 1)]["SpecificActivity"], PQ.SpecificActivity(1000.))

    def testTotalActivityCalculation(self):
        calculator = TotalActivityCalculator()
        calculator.invoke(self.dataIsotopeMultiAct)
        self.assertEqual(_global_data["det1"]["TotalActivity"], PQ.Activity(40.))

    def testTotalActivityCalculationDiffUnits(self):
        calculator = TotalActivityCalculator()
        data = {"det1": OrderedDict([(PQ.Isotope(3, 1), StoredData(PQ.Activity(10000., 10000., ureg.mBq))),
                                     (PQ.Isotope(2, 1), StoredData(PQ.Activity(30., 10., ureg.Bq)))])}
        calculator.invoke(data)
        self.assertEqual(_global_data["det1"]["TotalActivity"], PQ.Activity(40., sqrt(200.)))
