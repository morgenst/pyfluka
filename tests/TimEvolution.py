import unittest
from collections import OrderedDict
from utils import PhysicsQuantities as PQ
from base.StoredData import StoredData
from plugins.TimeEvolution import TimeEvolution


class TestTimeEvolution(unittest.TestCase):
    def setUp(self):
        pass

    def test_timeevolution_single_isotope(self):
        data = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.ProductionYield(10., 2.)))])}
        time_evo = TimeEvolution(None)
        time_evo.invoke(data)
        res = {"det1": OrderedDict([(PQ.Isotope(3, 1, 0), StoredData(PQ.ProductionYield(10. * 0.86020262228297506,
                                                                                        2.)))])}
        self.assertEqual(data, res)
