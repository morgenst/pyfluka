__author__ = 'morgenst'

from collections import OrderedDict

from pyfluka.base import _global_data, IllegalArgumentError

from BasePlugin import BasePlugin
from pyfluka.base.StoredData import StoredData
from pyfluka.reader import _dh
from pyfluka.utils import PhysicsQuantities as PQ


class SimpleCalculator(BasePlugin):
    """
    Base class for simple calculators defining common interface
    """
    # noinspection PyUnusedLocal
    def __init__(self, config=None):
        """
        Constructor
        :param config (dict): configuration
        :return:
        """
        pass

    def invoke(self, data):
        """
        Method invoking calculation
        :param data (dict): input data
        :return:
        """
        pass

    @staticmethod
    def _check_consistency(data, attr):
        """
        Method performing check if all required quantities for calculation are available in data
        :param data (dict): input data
        :param attr (list): quantities required by calculation
        :return:

        Raises:
            ValueError if any required quantity is missing
        """

        if isinstance(data, OrderedDict):
            if not all(elem.has_quantity(attr) for elem in data.values()):
                raise ValueError("Invalid input. Data object needs " + ", ".join(attr) + " but has " +
                                 ", ".join(data.values()[0].get_attributes()))
        elif isinstance(data, StoredData):
            if not data.has_quantity(attr):
                raise ValueError("Invalid input. Data object needs " + ", ".join(attr) + " but has " +
                                 ", ".join(data.get_attributes()))


class AoverLECalculator(SimpleCalculator):
    """
    Specific activity over LE calculator
    """
    # noinspection PyUnusedLocal
    def __init__(self, config=None):
        """
        Constructor
        :param config (dict): configuration
        :return:
        """
        self.quantity = PQ.AoverLE
        self._LE = None

    def invoke(self, data):
        """
        Entry point of calculation
        :param data (dict): input data
        :return:
        """
        self._LE = _dh._le
        for det in data.keys():
            self._calc(data[det])

    def _calc(self, data):
        """
        Performs calculation of A/LE
        :param data (dict): input data
        :return:

        Raises:
            ValueError if either Isotope or SpecificActivity are not in the input data
        """
        self._check_consistency(data, ['SpecificActivity'])
        try:
            self._check_consistency(data, ['SpecificActivity'])
        except Exception as e:
            raise e
        input_variables = zip(data.keys(), map(lambda x: x['SpecificActivity'], data.values()))
        for isotope, activity in input_variables:
            try:
                data[isotope].append(PQ.AoverLE(activity / self._LE[isotope]))
            except (KeyError, ZeroDivisionError):
                data[isotope].append(PQ.AoverLE(0.))


class SpecificActivityCalculator(SimpleCalculator):
    """
    Specific activity calculator: A/m
    """
    # noinspection PyUnusedLocal
    def __init__(self, config=None):
        """
        Constructor
        :param config (dict): configuration
        :return:
        """
        self.quantity = PQ.SpecificActivity

    def invoke(self, data):
        """
        Entry point for calculator
        :param data:
        :return:
        """
        for det in data.keys():
            try:
                mass = _global_data[det]["Mass"]
            except:
                raise IllegalArgumentError("Requested mass for detector " + det + ", but not available.")
            self._calc(data[det], mass)

    def _calc(self, data, mass):
        self._check_consistency(data, ['Activity'])
        for isotope, storedData in data.items():
            data[isotope].append(PQ.SpecificActivity(storedData["Activity"] / mass))


class TotalActivityCalculator(SimpleCalculator):
    # noinspection PyUnusedLocal
    def __init__(self, config=None):
        self.quantity = PQ.Activity

    def invoke(self, data):
        for det in data.keys():
            total_activity = self._calc(data[det].values())
            _global_data.add(det, "TotalActivity", total_activity)

    def _calc(self, data):
        return sum([elem["Activity"] for elem in data], PQ.Activity(0.))
