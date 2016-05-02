from pyfluka.base import InvalidInputError
from pyfluka.plugins.BasePlugin import BasePlugin
from pyfluka.utils import PhysicsQuantities as PQ


class Filter(BasePlugin):
    """
    Generic filter class
    """

    def __init__(self, **kwargs):
        """
        Constructor

        Required parameters:
        - quantity: quantity to be filtered on
        - threshold: either absolute or relative filter
            - absolute: requires unit compatible with quantity
            - relative: applies filter on relative contribute to sum
        :param dict kwargs: configuration parameter
        :raises InvalidInputError: if required arguments are not provided
        """
        try:
            self.quantity = kwargs["quantity"]
        except KeyError:
            raise InvalidInputError("Try to initialise Filter without specifying quantity.")
        try:
            try:
                self.threshold = float(kwargs["threshold"])
                self.type = "rel"
            except ValueError:
                self.threshold = PQ.create_generic(self.quantity + "Threshold", kwargs["threshold"])
                self.type = "abs"
        except KeyError:
            raise InvalidInputError("Try to initialise Filter without specifying threshold.")

    def invoke(self, data):
        for det, values in data.iteritems():
            data[det] = self._apply_filter(values)

    def _apply_filter(self, values):
        print values.items()[0][1][self.quantity]
        if self.type is "rel":
            total = sum(map(lambda kv: kv[1][self.quantity], values.iteritems()))
            return dict(filter(lambda kv: kv[1][self.quantity] / total > self.threshold, values.iteritems()))
        return dict(filter(lambda kv: kv[1][self.quantity] > self.threshold, values.iteritems()))
