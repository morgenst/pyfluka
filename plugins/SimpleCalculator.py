__author__ = 'morgenst'

from abc import ABCMeta, abstractmethod
from utils import PhysicsQuantities as PQ
from reader import _dh


class SimpleCalculator(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def invoke(self, data):
        pass

    def _checkConsistency(self, data, attr):
        if not set(data.keys()).issuperset(set(attr)):
            raise ValueError("Invalid input. Data object needs " + ", ".join(attr) + " but has " + ", ".join(data.keys()))

class AoverLECalculator(SimpleCalculator):
    def __init__(self):
        self.quantity = PQ.AoverLE

    def invoke(self, data):
        self._LE = _dh._LE
        for det in data.keys():
            self._calc(data[det])

    def _calc(self, data):
        self._checkConsistency(data, ['Isotope', 'SpecificActivity'])
        data['AoverLE'] = []
        for isotope, activity in zip(data['Isotope'], data['SpecificActivity']):
            data['AoverLE'].append(PQ.AoverLE(activity / self._LE[isotope]))
