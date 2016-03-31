from BasePlugin import BasePlugin
from base import _global_data, IllegalArgumentError


class SummationOperator(BasePlugin):
    def __init__(self, quantity, stored_quantity = None):
        self.quantity = quantity
        if stored_quantity:
            self.stored_quantity = stored_quantity
        else:
            self.stored_quantity = "Summed"+quantity

    def invoke(self, data):
        for det, values in data.items():
            if not values.values()[0].has_quantity(self.quantity):
                raise IllegalArgumentError("Request to sum " + self.quantity + " which is not stored.")
            _global_data.add(det, self.stored_quantity, sum(list(map(lambda e: e[self.quantity], values.values()))))
