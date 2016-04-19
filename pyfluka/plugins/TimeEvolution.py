from math import exp, log

from pyfluka.base import IllegalArgumentError
from pyfluka.plugins.BasePlugin import BasePlugin
from pyfluka.reader import _dh
from pyfluka.utils import PhysicsQuantities as PQ


class TimeEvolution(BasePlugin):
    """
    Plugin for time evolution of production yields
    """
    def __init__(self, **kwargs):
        if "irr_time" not in kwargs or "cool_time" not in kwargs:
            raise IllegalArgumentError("Unable to instantiate TimeEvolution. Either irr_time or cool_time missing.")
        self.cool_time = self._parse_config(kwargs.pop('cool_time'))
        self.irr_time = self._parse_config(kwargs.pop('irr_time'))

    def invoke(self, data):
        """
        Call method. Initiates calculation

        :param dict data: dictionary holding data to be processed
        :return:
        """
        for det in data.keys():
            self._apply_coefficient(data[det])

    def _apply_coefficient(self, data):
        """
        Application of time evolution coefficients on production yield

        :param dict data: scoring region specific dictionaries with isotopes as key
        :return:
        """
        for k, val in data.iteritems():
            val["ProductionYield"] *= self._calculate_evolution_coeff(k)

    def _calculate_evolution_coeff(self, isotope):
        """
        Simple time evolution based on exp. decay and build up model.

        :param Isotope isotope: isotope
        :return: time evolution factor
        :rtype: float
        """
        half_life = _dh._hl[isotope]
        return max(0., (1. - exp(-log(2.) * self.irr_time / half_life)) * exp(-log(2.) * self.cool_time / half_life))

    @staticmethod
    def _parse_config(time):
        ts = time.split(" ")
        return PQ.Time(float(ts[0]), 0., PQ.Time._get_conversion_dict()[ts[1]])
