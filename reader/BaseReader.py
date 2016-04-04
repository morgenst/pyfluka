import importlib
from base import IllegalArgumentError
from utils import ureg


class BaseReader(object):
    def __init__(self, quantity, dim, weights):
        """
        Constructor for reader of RESNUClei scored data
        :param quantity (str): physics quantity scored; defaults to Activity
        :param dim (str): dimension of scored quantity
        :return:
        """
        m = importlib.import_module("utils.PhysicsQuantities")
        if dim is not None:
            self.dim = ureg(dim)
        self.pq = getattr(m, quantity)
        self.weights = weights

    def load(self, files):
        if isinstance(files, list):
            merged_data = None
            for file_name in files:
                weight = 1.
                if self.weights:
                    weight = self.weights.pop(0)
                data = self._load(file_name, weight)
                if merged_data:
                    self.__class__._merge(merged_data, data)
                else:
                    merged_data = data
            return merged_data
        elif isinstance(files, str):
            weight = 1.
            if self.weights:
                weight = self.weights.pop(0)
            return self._load(files, weight)
        else:
            raise IllegalArgumentError("Received unsupported type for input files: " + str(type(files)))