import pickle
import os
from pkg_resources import resource_stream


def load(filename):
    f = resource_stream(__name__, filename)
    obj = pickle.load(f)
    f.close()
    return obj


def lazyprop(fn):
    attr_name = "_lazy_" + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


class DataHandle(object):
    def __init__(self):
        pass

    @lazyprop
    def _le(self):
        return load("../data/LEDB.p")

    @lazyprop
    def _h10(self):
        return load("../data/Activity_H10_conversion.p")

    @lazyprop
    def _hp007(self):
        return load("../data/Activity_Hp007_conversion.p")

    @lazyprop
    def _einh(self):
        return load("../data/inhalation.p")

    @lazyprop
    def _eing(self):
        return load("../data/ingestion.p")

    @lazyprop
    def _hl(self):
        return load("../data/half_lifes.p")
