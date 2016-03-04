__author__ = 'morgenst'

from BasePlugin import BasePlugin
from utils import PhysicsQuantities as PQ
from reader import _dh
#from numpy import sum

class SimpleCalculator(BasePlugin):
    def __init__(self, config = None):
        pass

    def invoke(self, data):
        pass

    def _checkConsistency(self, data, attr):
        print data
        if not set(data.keys()).issuperset(set(attr)):
            raise ValueError("Invalid input. Data object needs " + ", ".join(attr) + " but has " + ", ".join(data.keys()))


class AoverLECalculator(SimpleCalculator):
    def __init__(self, config = None):
        self.quantity = PQ.AoverLE

    def invoke(self, data):
        self._LE = _dh._LE
        for det in data.keys():
            self._calc(data[det])

    def _calc(self, data):
        self._checkConsistency(data, ['Isotope', 'SpecificActivity'])
        data['AoverLE'] = []
        for isotope, activity in zip(data['Isotope'], data['SpecificActivity']):
            try:
                data['AoverLE'].append(PQ.AoverLE(activity / self._LE[isotope]))
            except KeyError:
                data['AoverLE'].append(0.)


class SpecificActivityCalculator(SimpleCalculator):
    def __init__(self, config = None):
        self.quantity = PQ.SpecificActivity

    def invoke(self, data):
        for det in data.keys():
            self._calc(data[det])

    def _calc(self, data):
        self._checkConsistency(data, ['Activity'])
        mass = PQ.Mass(1.)
        if data.has_key("Mass"):
            mass = data['Mass']
        data['SpecificActivity'] = []
        for activity in data['Activity']:
            data['SpecificActivity'].append(PQ.SpecificActivity(activity / mass))


class TotalActivityCalculator(SimpleCalculator):
    def __init__(self, config = None):
        self.quantity = PQ.Activity

    def invoke(self, data):
        for det in data.keys():
            self._calc(data[det])

    def _calc(self, data):
        self._checkConsistency(data, ['Activity'])
        data["TotalActivity"] = sum(data["Activity"], PQ.Activity(0.))