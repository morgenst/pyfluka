__author__ = 'marcusmorgenstern'
__mail__ = ''

import pickle
import re
from abc import ABCMeta, abstractmethod
from copy import deepcopy, copy
from numbers import Number

from numpy import sqrt
from pkg_resources import resource_stream

from pyfluka.base import IllegalArgumentError
from pyfluka.utils import ureg

f = resource_stream(__name__, "../data/periodic_table.p")
_periodic_table = pickle.load(f)
f.close()


class AbsPhysicsQuantity(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, val, unc, unit, symbol = None):
        if issubclass(type(val), AbsPhysicsQuantity):
            self.val = copy(val.val)
            self.unc = copy(val.unc)
        elif isinstance(val, str) and unc == 0:
            self.val = ureg.Quantity(val)
            self.unc = ureg.Quantity(0., self.val.units)
        elif not isinstance(val, ureg.Quantity):
            self.val = val * ureg.Quantity(unit)
            self.unc = unc * ureg.Quantity(unit)
        else:
            self.val = val
            if isinstance(unc, ureg.Quantity):
                self.unc = unc
            else:
                self.unc = ureg.Quantity(unc, self.val.units)
        self._symbol = symbol

    def __setstate__(self, state):
        self.val = ureg.Quantity(state['val'].magnitude, state['val'].units)
        self.unc = ureg.Quantity(state['unc'].magnitude, state['unc'].units)

    def __deepcopy__(self, memo):
        obj = type(self)(self.val, self.unc)
        obj.__dict__.update(self.__dict__)
        return obj

    def __eq__(self, other):
        return self.val == other.val and self.unc == other.unc

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Number):
            if other == 0.:
                return deepcopy(self)
            else:
                raise IllegalArgumentError("Invalid request for addition of " + str(self) + " and " + str(other))
        if not type(self) == type(other):
            raise IllegalArgumentError("Invalid request for addition of " + str(self) + " and " + str(other))
        val = self.val + other.val
        unc = sqrt(pow(self.unc, 2) + pow(other.unc, 2))
        assert(val.units == unc.units)
        return self.__class__(val, unc)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Number):
            if other == 0.:
                return deepcopy(self)
            else:
                raise IllegalArgumentError("Invalid request for subtraction of " + str(self) + " and " + str(other))
        if not type(self) == type(other):
            raise IllegalArgumentError("Invalid request for subtraction of " + str(self) + " and " + str(other))
        val = self.val - other.val
        unc = 0. * val #sqrt(pow(self.unc, 2) + pow(other.unc, 2))
        assert (val.units == unc.units)
        return self.__class__(val, unc)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return self.__scalar_mul__(other)
        elif isinstance(other, self.__class__):
            return self.__class__(self.val * other.val, self.unc * other.unc)
        elif issubclass(type(other), AbsPhysicsQuantity):
            tmp = deepcopy(self)
            tmp.val = self.val * other.val
            tmp.unc = ureg.Quantity(-1., self.val.units * other.val.units)
            return tmp

    def __scalar_mul__(self, other):
        return self.__class__(self.val * other, self.unc)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, Number):
            return self.__class__(self.val / other, self.unc)
        else:
            return create_generic(self.__class__.__name__ + "Over" + other.__class__.__name__,
                                  self.val / other.val)

    def __rdiv__(self, other):
        if isinstance(other, Number):
            return create_generic("Inverse" + self.__class__.__name__, other / self.val)

    def __abs__(self):
        return self.__class__(abs(self.val), abs(self.unc))

    def __str__(self):
        return format(self)

    def __le__(self, other):
        return self.val <= other.val

    def __lt__(self, other):
        return self.val < other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __gt__(self, other):
        return self.val > other.val

    def __format__(self, spec):
        if "L" in spec:
            spec = spec.replace("L", "")
            return self._latex_format(spec)
        magnitude_str = format(self.val, spec)
        unc_str = format(self.unc)
        default_str = self.__class__.__name__ + ": %s +- %s" % (magnitude_str, unc_str)
        return default_str

    def _latex_format(self, spec):
        """
        Latex formatting options.
        formatting options:
            - nu: no units
            - ne: no uncertainty
            - s: symbol character
            - su: symbol character and unit

        :param spec: formatting option
        :return: formatted string
        :rtype: string
        """
        no_uncertainty = False
        no_unit = False
        if "ne" in spec:
            spec = spec.replace("ne", "")
            no_uncertainty = True
        if "nu" in spec:
            spec = spec.replace("nu", "")
            no_unit = True
        if "s" in spec:
            return self._latex_format_symbol(spec.replace("s", ""))
        magnitude_str = format(self.val, spec)
        unc_str = format(self.unc, spec)
        if no_uncertainty:
            ret = "$%s$" % magnitude_str
        else:
            ret = "$%s \\pm %s$" % (magnitude_str, unc_str)

        if no_unit:
            unit_str = str(self.val.units)
            ret = ret.replace(unit_str, "")
        ret = re.sub("\s+", " ", ret)
        return ret

    def _latex_format_symbol(self, spec):
        """
        Latex formatting symbol representation

        :param spec: formatting option
        :return: formatted string
        :rtype: string
        """
        if "u" in spec:
            return "%s [$%s$]" % (self._symbol if self._symbol else "", '{:~L}'.format(self.val.units))

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
        return self.__class__.__name__ + "%i-%s-%s" % (self.A, iso_str, _periodic_table[self.Z - 1])

    def __str__(self):
        return format(self)


class Activity(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.Bq):
        super(self.__class__, self).__init__(val, unc, unit, "A")


class SpecificActivity(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.Bq / ureg.kg):
        super(self.__class__, self).__init__(val, unc, unit, "A")


class ExemptionLimit(AbsPhysicsQuantity):
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


class EInh(AbsPhysicsQuantity):
    def __init__(self, val, unit=ureg.Sv / ureg.Bq):
        super(self.__class__, self).__init__(val, 0., unit)


class EIng(AbsPhysicsQuantity):
    def __init__(self, val, unit=ureg.Sv / ureg.Bq):
        super(self.__class__, self).__init__(val, 0., unit)


class Dose(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.Sv):
        super(self.__class__, self).__init__(val, unc, unit)


class ProductionYield(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=1. / ureg.second):
        super(self.__class__, self).__init__(val, unc, unit)


class Time(AbsPhysicsQuantity):
    def __init__(self, val, unc=0., unit=ureg.second):
        super(self.__class__, self).__init__(val, unc, unit)

    @staticmethod
    def _get_conversion_dict():
        return {"s": ureg.second,
                "m": ureg.minute,
                "h": ureg.hour,
                "w": ureg.week,
                "y": ureg.year}


def create_generic(name, val, unc=0, unit=ureg.dimensionless):
    def __init__(self, val, unc, unit=ureg.dimensionless):
        super(self.__class__, self).__init__(val, unc, unit)
    c = type(name, (AbsPhysicsQuantity,), {"__init__": __init__})
    c._symbol = ""
    return c(val, unc, unit)

