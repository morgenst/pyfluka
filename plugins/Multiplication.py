import importlib
import pkgutil
from ast import literal_eval
from base import InvalidInputError
from BasePlugin import BasePlugin


class MultiplicationOperator(BasePlugin):
    def __init__(self, *args, **kwargs):
        try:
            setattr(self, kwargs['type'], True)
            self.multiplier = kwargs['multiplier']
            tmp_multiplicand = kwargs['multiplicand']
            if tmp_multiplicand.count("const"):
                self.multiplicand = float(tmp_multiplicand.replace("const:", ""))
            elif tmp_multiplicand.count("builtin"):
                self.multiplicand = self.find_builtin(tmp_multiplicand.replace("builtin:", ""))
            self.product = kwargs['product'].split(":")[0]
            m = importlib.import_module("utils.PhysicsQuantities")
            self.quantity = getattr(m, kwargs['product'].split(":")[-1])
        except KeyError:
            raise InvalidInputError("Unable to initialise multiplication operator")

    def invoke(self, data):
        for det in data.keys():
            if hasattr(self, "scalar"):
                self._scalar_multiplication(data[det])
            elif hasattr(self, "dict"):
                print self._dict_multiplication(data[det])

    def _scalar_multiplication(self, data):
        for k, v in data.iteritems():
            v.append(**{self.product: v[self.multiplier] * self.multiplicand})

    def _dict_multiplication(self, data):
        default = 0.
        for k, v in data.iteritems():
            v.append(**{self.product: self.quantity(v[self.multiplier] * self.multiplicand.get(k, default))})

    def find_builtin(self, builtin):
        from reader import _dh
        try:
            func = getattr(_dh, builtin)
        except AttributeError:
            pass
        try:
            func = getattr(_dh, "_" + builtin)
        except AttributeError:
            pass
        return func
