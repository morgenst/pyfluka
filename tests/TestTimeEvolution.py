import unittest
from collections import OrderedDict
from math import exp, log

from pyfluka.base import IllegalArgumentError
from pyfluka.utils import ureg

from pyfluka.base.StoredData import StoredData
from pyfluka.plugins.TimeEvolution import TimeEvolution
from pyfluka.reader import _dh
from pyfluka.utils import PhysicsQuantities as PQ


class TestTimeEvolution(unittest.TestCase):
    def setUp(self):
        self.config = {"irr_time": "1 y", "cool_time": "1 y"}

    def test_config_parsing(self):
        time_evo = TimeEvolution(**self.config)
        self.assertEqual(time_evo.irr_time, PQ.Time(1., 0., ureg.year))
        self.assertEqual(time_evo.cool_time, PQ.Time(1., 0., ureg.year))

    def test_config_missing_irr_time(self):
        config = {"irr_time": "1 y"}
        self.assertRaises(IllegalArgumentError, TimeEvolution, **config)

    def test_config_missing_cool_time(self):
        config = {"cool_time": "1 y"}
        self.assertRaises(IllegalArgumentError, TimeEvolution, **config)

    def test_time_evolution_simple(self):
        isotope = PQ.Isotope(3, 1, 0)
        data = {"det1": OrderedDict([(isotope, StoredData(PQ.ProductionYield(10., 2.)))])}
        time_evo = TimeEvolution(**self.config)
        time_evo.invoke(data)
        res = (1 - exp(-log(2) * PQ.Time(1, unit=ureg.year) / _dh._hl[isotope])) \
              * exp(-log(2) * PQ.Time(1, unit=ureg.year)/ _dh._hl[isotope]) * PQ.ProductionYield(10., 2.)
        self.assertEqual(data["det1"][PQ.Isotope(3, 1, 0)]["ProductionYield"], res)


