from BasePlugin import BasePlugin
from pyfluka.base import _global_data, IllegalArgumentError


class SummationOperator(BasePlugin):
    """
    Summation operator
    """
    def __init__(self, quantity, stored_quantity=None):
        """
        Constructor

        :param PhysicsQuantity quantity: quantity to be summed
        :param PhysicsQuantity stored_quantity: quantity to store result in
        """
        self.quantity = quantity
        if stored_quantity:
            self.stored_quantity = stored_quantity
        else:
            self.stored_quantity = "Summed"+quantity

    def invoke(self, data):
        """
        Performing calculation

        :param dict data: data dictionary
        :return:
        """
        for det, values in data.items():
            if not values.values()[0].has_quantity(self.quantity):
                raise IllegalArgumentError("Request to sum " + self.quantity + " which is not stored.")
            _global_data.add(det, self.stored_quantity, sum(list(map(lambda e: e[self.quantity], values.values()))))
