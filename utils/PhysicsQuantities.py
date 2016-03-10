__author__ = 'marcusmorgenstern'
__mail__ = ''

import pickle
from utils import ureg
from abc import ABCMeta, abstractmethod
from numpy import sqrt

f = open("../data/periodic_table.p")
_periodic_table = pickle.load(f)
f.close()


class AbsPhysicsQuantity:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, val, unc, unit):
        if not isinstance(val, ureg.Quantity):
            self.val = val * ureg.Quantity(unit)
            self.unc = unc * ureg.Quantity(unit)
        else:
            self.val = val
            if isinstance(unc, ureg.Quantity):
                self.unc = unc
            else:
                self.unc = ureg.Quantity(unc, self.val.units)

    def __setstate__(self, state):
        self.val = ureg.Quantity(state['val'].magnitude, state['val'].units)
        self.unc = ureg.Quantity(state['unc'].magnitude, state['unc'].units)

    def __eq__(self, other):
        return self.val == other.val and self.unc == other.unc

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        val = self.val + other.val
        unc = sqrt(pow(self.unc, 2) + pow(other.unc, 2))
        assert(val.units == unc.units)
        return self.__class__(val, unc)

    def __radd__(self, other):
        return other.__add__(self)

    def __div__(self, other):
        return self.val / other.val

    def __str__(self):
        return format(self)

    def __format__(self, spec):
        if "L" in spec:
            spec = spec.replace("L", "")
            magnitude_str = format(self.val, spec)
            unc_str = format(self.unc)
            ret = "$%s \\pm %s$" % (magnitude_str, unc_str)
            return ret
        magnitude_str = format(self.val, spec)
        unc_str = format(self.unc)
        default_str = self.__class__.__name__ + ": %s +- %s" % (magnitude_str, unc_str)
        return default_str

    def __float__(self):
        return float(self.val.magnitude)


class Isotope:
    # noinspection PyPep8Naming,PyPep8Naming
    def __init__(self, A=-1, Z="", iso=0):
        if type(Z) == str and Z > 0:
            self.Z = _periodic_table.index(Z) + 1
        elif type(Z) == int:
            self.Z = Z
        else:
            raise ValueError("Invalid input for Isotope. Z given as " + type(Z))
        self.A = int(A)
        self.iso = int(iso)

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

    def __format__(self, spec):
        iso_str = "m" if self.iso > 0 else ""
        if "L" in spec:
            spec = spec.replace("L", "")
            ret = "$^{%i%s}$%s" % (self.A, iso_str, _periodic_table[self.Z - 1])
            return ret
        return self.__class__.__name__ + "%i-%s-%s" % (self.A, iso_str, _periodic_table[self.Z])

    def __str__(self):
        return format(self)


class Activity(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.Bq):
        super(self.__class__, self).__init__(val, unc, unit)


class SpecificActivity(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.Bq / ureg.kg):
        super(self.__class__, self).__init__(val, unc, unit)


class ExcemptionLimit(AbsPhysicsQuantity):
    def __init__(self, val, unit=ureg.Bq / ureg.kg):
        super(self.__class__, self).__init__(val, 0., unit)

    def __str__(self):
        return "LE"


class AoverLE(AbsPhysicsQuantity):
    def __init__(self, val, unc=0.):
        super(self.__class__, self).__init__(val, unc, ureg.dimensionless)

    def __str__(self):
        return "A/LE"


class DoseRate(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.Sv):
        super(self.__class__, self).__init__(val, unc, unit)

    def __str__(self):
        return "D"


class H10(AbsPhysicsQuantity):
    def __init__(self, val, unit=ureg.Bq / (ureg.mSv / ureg.hour)):
        super(self.__class__, self).__init__(val, 0., unit)

    def __str__(self):
        return "H10: " + str(self.quantity)


class Hp007(AbsPhysicsQuantity):
    def __init__(self, val, unit=ureg.Bq / (ureg.mSv / ureg.hour)):
        super(self.__class__, self).__init__(val, 0., unit)

    def __str__(self):
        return "Hp007"


class Mass(AbsPhysicsQuantity):
    def __init__(self, val, unit=ureg.kg):
        super(self.__class__, self).__init__(val, 0., unit)

    #def __str__(self):
    #    return "m"
