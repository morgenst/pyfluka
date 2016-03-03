import unittest
import utils.PhysicsQuantities as PQ
from plugins.SimpleCalculator import AoverLECalculator, SpecificActivityCalculator
from utils import ureg


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.dataIsotopeSpecificAct = {"det1": {'Isotope': [PQ.Isotope(3, 1)], 'SpecificActivity': [PQ.SpecificActivity(10.)]}}
        self.dataIsotopeAct = {"det1": {'Mass' : PQ.Mass(10., ureg.kg), 'Isotope': [PQ.Isotope(3, 1)], 'Activity': [PQ.Activity(10.)]}}
        self.AoverLECalculator = AoverLECalculator()

    def testAoverLESimple(self):
        self.AoverLECalculator.invoke(self.dataIsotopeSpecificAct)
        self.assertEqual(self.dataIsotopeSpecificAct["det1"]["AoverLE"], [PQ.AoverLE(10. / 2.00E+005)])

    def testAoverLEWrongInput(self):
        self.assertRaises(ValueError, self.AoverLECalculator.invoke, {"det1": {'Isotope': [], 'Activity': []}})

    def testSpecificActivitySimple(self):
        calculator = SpecificActivityCalculator()
        calculator.invoke(self.dataIsotopeAct)
        tmp = PQ.SpecificActivity(1.)
        self.assertEqual(self.dataIsotopeAct["det1"]["SpecificActivity"], [PQ.SpecificActivity(1.)])