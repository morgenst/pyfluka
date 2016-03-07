import unittest
import utils.PhysicsQuantities as PQ
from plugins.SimpleCalculator import *
from utils import ureg
from math import sqrt


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.dataIsotopeSpecificAct = {"det1": {'Isotope': [PQ.Isotope(3, 1)],
                                                'SpecificActivity': [PQ.SpecificActivity(10.)]}}
        self.dataIsotopeAct = {"det1": {'Mass': PQ.Mass(10., ureg.kg),
                                        'Isotope': [PQ.Isotope(3, 1)],
                                        'Activity': [PQ.Activity(10.)]}}
        self.dataIsotopeMultiAct = {"det1": {'Mass': PQ.Mass(10., ureg.kg),
                                             'Isotope': [PQ.Isotope(3, 1)],
                                             'Activity': [PQ.Activity(10.), PQ.Activity(30.)]}}
        self.AoverLECalculator = AoverLECalculator()

    def testAoverLESimple(self):
        self.AoverLECalculator.invoke(self.dataIsotopeSpecificAct)
        self.assertEqual(self.dataIsotopeSpecificAct["det1"]["AoverLE"], [PQ.AoverLE(10. / 2.00E+005)])

    @unittest.skip("Not implemented")
    def testAoverLENonExistingLimit(self):
        pass

    def testAoverLEWrongInput(self):
        self.assertRaises(ValueError, self.AoverLECalculator.invoke, {"det1": {'Isotope': [], 'Activity': []}})

    def testSpecificActivitySimple(self):
        calculator = SpecificActivityCalculator()
        calculator.invoke(self.dataIsotopeAct)
        self.assertEqual(self.dataIsotopeAct["det1"]["SpecificActivity"], [PQ.SpecificActivity(1.)])

    def testSpecificActivitySimpleDiffMassUnit(self):
        data = self.dataIsotopeAct
        data["det1"]["Mass"] = PQ.Mass(10., ureg.g)
        calculator = SpecificActivityCalculator()
        calculator.invoke(data)
        self.assertEqual(self.dataIsotopeAct["det1"]["SpecificActivity"], [PQ.SpecificActivity(1000.)])

    def testTotalActivityCalculation(self):
        calculator = TotalActivityCalculator()
        calculator.invoke(self.dataIsotopeMultiAct)
        self.assertEqual(self.dataIsotopeMultiAct["det1"]["TotalActivity"], PQ.Activity(40.))

    def testTotalActivityCalculationDiffUnits(self):
        calculator = TotalActivityCalculator()
        data = {"det1": {'Activity': [PQ.Activity(10000., 10000., ureg.mBq), PQ.Activity(30., 10., ureg.Bq)]}}
        calculator.invoke(data)
        self.assertEqual(data["det1"]["TotalActivity"], PQ.Activity(40., sqrt(200.)))
