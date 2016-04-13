import importlib
from functools import partial

from BasePlugin import BasePlugin
from pyfluka.base import InvalidInputError, _global_data, IllegalArgumentError
from pyfluka.utils import PhysicsQuantities as PQ


class MultiplicationOperator(BasePlugin):
    def __init__(self, *args, **kwargs):
        try:
            setattr(self, kwargs['type'], True)
            self.multiplier = kwargs['multiplier']
            tmp_multiplicand = kwargs['multiplicand']
            if tmp_multiplicand.count("const"):
                tmp_multiplicand = tmp_multiplicand.replace("const:", "")
                try:
                    self.multiplicand = float(tmp_multiplicand)
                except ValueError:
                    self.multiplicand = PQ.create_generic("multiplicand", tmp_multiplicand)
            elif tmp_multiplicand.count("builtin"):
                self.multiplicand = self.find_builtin(tmp_multiplicand.replace("builtin:", ""))
            elif tmp_multiplicand.count("global:"):
                if tmp_multiplicand.count("mass"):
                    self.multiplicand = "mass"
                    self.dict = True
                else:
                    self.multiplicand = _global_data[tmp_multiplicand.replace("global:", "")]
                    self.scalar = True
            else:
                self.multiplicand = tmp_multiplicand
            self.product = kwargs['product'].split(":")[0]
            m = importlib.import_module("pyfluka.utils.PhysicsQuantities")
            try:
                self.quantity = getattr(m, kwargs['product'].split(":")[-1])
            except AttributeError:
                self.quantity = partial(getattr(m, 'create_generic'), kwargs['product'].split(":")[-1])
            self.current_detector = None
        except KeyError:
            raise InvalidInputError("Unable to initialise multiplication operator")

    def invoke(self, data):
        for det in data.keys():
            self.current_detector = det
            if hasattr(self, "scalar"):
                self._scalar_multiplication(data[det])
            elif hasattr(self, "dict"):
                self._dict_multiplication(data[det])

    def _scalar_multiplication(self, data):
        for k, v in data.iteritems():
            v.append(**{self.product: v[self.multiplier] * self.multiplicand})

    def _dict_multiplication(self, data):
        default = 0.
        for k, v in data.iteritems():
            if isinstance(self.multiplicand, str):
                #TODO: this is a division!!!!
                if self.multiplicand == "mass":
                    v.append(**{self.product: self.quantity(v[self.multiplier] /
                                                            _global_data[self.current_detector]["mass"])})
                else:
                    v.append(**{self.product: self.quantity(v[self.multiplier] * v[self.multiplicand])})
            else:
                v.append(**{self.product: self.quantity(v[self.multiplier] * self.multiplicand.get(k, default))})

    def find_builtin(self, builtin):
        from pyfluka.reader import _dh
        func = None
        try:
            func = getattr(_dh, builtin)
        except AttributeError:
            pass
        try:
            func = getattr(_dh, "_" + builtin)
        except AttributeError:
            pass
        if not func:
            raise IllegalArgumentError("Requested builtin " + builtin + " could not be found.")
        return func
