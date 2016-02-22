import unittest
import utils.PhysicsQuantities as PQ
from plugins.SimpleCalculator import AoverLECalculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.data = {"det1": {'Isotope': [PQ.Isotope(3, 1)], 'SpecificActivity': [PQ.SpecificActivity(10.)]}}
        self.AoverLECalculator = AoverLECalculator()

    def testAoverLESimple(self):
        self.AoverLECalculator.invoke(self.data)
        self.assertEqual(self.data["det1"]["AoverLE"], [PQ.AoverLE(10./2.00E+005)])

    def testAoverLEWrongInput(self):
        self.assertRaises(ValueError, self.AoverLECalculator.invoke, {"det1": {'Isotope': [], 'Activity': []}})
