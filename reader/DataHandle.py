import pickle


def load(fName):
    f = open(fName, "r")
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
    def _LE(self):
        return load("../data/LEDB.p")

    @lazyprop
    def _H10(self):
        return load("../data/Activity_H10_conversion.p")

    @lazyprop
    def _Hp007(self):
        return load("../data/Activity_Hp007_conversion.p")
