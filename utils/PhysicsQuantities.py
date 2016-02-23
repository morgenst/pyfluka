__author__ = 'marcusmorgenstern'
__mail__ = ''

import pickle
from utils import ureg
from abc import ABCMeta, abstractmethod

f = open("../data/periodic_table.p")
_periodic_table = pickle.load(f)
f.close()


class AbsPhysicsQuantity:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, val, unc, unit):
        self.val = val * ureg.Quantity(unit)
        self.unc = unc * ureg.Quantity(unit)

    @abstractmethod
    def __str__(self):
        return None

    def __setstate__(self, state):
        self.val = ureg.Quantity(state['val'].magnitude, state['val'].units)
        self.unc = ureg.Quantity(state['unc'].magnitude, state['unc'].units)

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __div__(self, other):
        return self.val / other.val

    def __str__(self):
        return str(self.val.magnitude)

    def __float__(self):
        return self.val.magnitude

class Isotope:
    def __init__(self, A = -1, Z = "", iso = 0):
        self.unit = ureg.dimensionless
        if type(Z) == str and Z > 0:
            self.Z = _periodic_table.index(Z) + 1
        elif type(Z) == int:
            self.Z = Z
        else:
            raise ValueError("Invalid input for Isotope. Z given as " + type(Z))
        self.A = A
        self.iso = iso

    def __hash__(self):
        return hash((self.A, self.Z, self.iso))

    def __eq__(self, other):
        if self.A != other.A:
            return False
        if self.Z != other.Z:
            return False
        if self.iso != other.iso:
            return False
        return True

    def __str__(self):
        return "Isotope"


class Activity(AbsPhysicsQuantity):
    def __init__(self, val, unc = 0., unit=ureg.Bq):
        super(self.__class__, self).__init__(val, unc, unit)

    #def __str__(self):
    #    return str(self.val)


class SpecificActivity(AbsPhysicsQuantity):
    def __init__(self, val, unc = 0., unit=ureg.Bq / ureg.kg):
        super(self.__class__, self).__init__(val, unc, unit)

    def __str__(self):
        return "A"


class ExcemptionLimit(AbsPhysicsQuantity):
    def __init__(self, val, unit = ureg.Bq / ureg.kg):
        super(self.__class__, self).__init__(val, 0., unit)

    def __str__(self):
        return "LE"

class AoverLE(AbsPhysicsQuantity):
    def __init__(self, val, unc = 0., unit=ureg.dimensionless):
        super(self.__class__, self).__init__(val, unc, unit)

    def __str__(self):
        return "A/LE"


class DoseRate(AbsPhysicsQuantity):
    def __init__(self, val, unc = 0., unit = ureg.Sv):
        super(self.__class__, self).__init__(val, unc, unit)

    def __str__(self):
        return "D"


class H10(AbsPhysicsQuantity):
    def __init__(self, val, unit = ureg.Bq / (ureg.mSv / ureg.hour)):
        super(self.__class__, self).__init__(val, 0., unit)

    def __str__(self):
        return "H10: " + str(self.quantity)


class Hp007(AbsPhysicsQuantity):
    def __init__(self, val, unit = ureg.Bq / (ureg.mSv / ureg.hour)):
        super(self.__class__, self).__init__(val, 0., unit)

    def __str__(self):
        return "Hp007"