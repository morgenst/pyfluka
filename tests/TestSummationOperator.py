import unittest
from plugins.Summation import SummationOperator
from utils import PhysicsQuantities as PQ
from base.StoredData import StoredData
from base import _global_data, IllegalArgumentError


class TestSummationOperator(unittest.TestCase):
    def setUp(self):
        self.sum_op = SummationOperator("Activity")
        self.single_det_data = {"det1": {PQ.Isotope(3, 1, 0): StoredData(PQ.Activity(10.)),
                                         PQ.Isotope(3, 2, 0): StoredData(PQ.Activity(15.))}}

    def test_config_parse_default_params(self):
        sum_op = SummationOperator("Activity")
        self.assertEqual(sum_op.quantity, "Activity")
        self.assertEqual(sum_op.stored_quantity, "SummedActivity")

    def test_config_parse_custom_params(self):
        sum_op = SummationOperator("Activity", "TotalActivity")
        self.assertEqual(sum_op.quantity, "Activity")
        self.assertEqual(sum_op.stored_quantity, "TotalActivity")

    def test_calculation_single_detector(self):
        self.sum_op.invoke(self.single_det_data)
        self.assertEqual(_global_data["det1"]["SummedActivity"], PQ.Activity(25.))

    def test_calculation_single_detector_custom_name(self):
        sum_op = SummationOperator("Activity", "TotalActivity")
        sum_op.invoke(self.single_det_data)
        self.assertEqual(_global_data["det1"]["TotalActivity"], PQ.Activity(25.))

    def test_exception_request_non_existing_quantity(self):
        sum_op = SummationOperator("Dose")
        self.assertRaises(IllegalArgumentError, sum_op.invoke, self.single_det_data)
