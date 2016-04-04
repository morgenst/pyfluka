from BasePlugin import BasePlugin
from reader import _dh


class Decorator(BasePlugin):
    def __init__(self, config):
        self.config = config
        self.quantities = [getattr(_dh, "_"+c.lower()) for c in config]

    def invoke(self, data):
        for det in data.keys():
            self._add_quantities(data[det])

    #TODO: check for default constructor call in case of default initialisation
    def _add_quantities(self, data):
        for k, v in data.iteritems():
            for quantity in self.quantities:
                v.append(quantity.get(k, quantity.values()[0].__class__(0.)))
