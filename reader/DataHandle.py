import pickle


def load(filename):
    f = open(filename, "r")
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
