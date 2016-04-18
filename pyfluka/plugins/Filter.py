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
            except ValueError:
                self.threshold = PQ.create_generic(self.quantity + "Threshold", kwargs["threshold"])
        except KeyError:
            raise InvalidInputError("Try to initialise Filter without specifying threshold.")
        self.type = "rel"

    def invoke(self, data):
        for det, values in data.iteritems():
            data[det] = self._apply_filter(values)

    def _apply_filter(self, values):
        return dict(filter(lambda kv: kv[1][self.quantity] > self.threshold, values.iteritems()))
