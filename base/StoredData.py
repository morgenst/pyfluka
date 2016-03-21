__author__ = 'marcusmorgenstern'
__mail__ = ''

from collections import OrderedDict, defaultdict


class GlobalData:
    def __init__(self):
        self.data = defaultdict(dict)

    def add(self, *args):
        self._add_impl(self.data, args[:-1], args[-1])

    def _add_impl(self, data, args, val):
        if len(args) == 1:
            data[args[0]] = val
        else:
            self._add_impl(data[args[0]], args[1:], val)

    def __eq__(self, other):
        if not isinstance(other, dict):
            return False
        return self.data == other

    def __getitem__(self, item):
        if isinstance(item, str):
            if item in self.data:
                return self.data[item]
            else:
                raise KeyError("Requested information " + item + " not stored in global data")


class StoredData:
    def __init__(self, *args, **kwargs):
        self.data = OrderedDict()
        for arg in args:
            self.data[arg.__class__.__name__] = arg
        for k, v in kwargs.items():
            self.data[k] = v

    def __eq__(self, other):
        return self.data == other.data

    def __getitem__(self, item):
        """
        Overwritten access operator
        :param item (str): key for value
        :return: stored quantity for item; None if item not in __dict__
        """
        if isinstance(item, list):
            return [self.data[i] for i in item]
        if item in self.data:
            return self.data[item]
        return None

    def __setitem__(self, key, value):
        """
        Overwritten setter operator
        :param key (str): key for value to be set
        :param value: value to be assigned for key
        :return:
        """
        self.data[key] = value

    def append(self, *args, **kwargs):
        if all(isinstance(arg, list) for arg in args) and args:
            raise ValueError("List items are not supported to be added.")
        for arg in args:
            if arg.__class__.__name__ in self.data:
                self.data[arg.__class__.__name__] += arg
            else:
                self.data[arg.__class__.__name__] = arg
        for k, v in kwargs.items():
            self.data[k] = v

    def has_quantity(self, quantaties):
        if isinstance(quantaties, list):
            return set(self.data.keys()).issuperset(set(quantaties))
        return quantaties in self.data.keys()

    def get_attributes(self):
        return self.data.keys()

    def __add__(self, other):
        for k in self.data.keys():
            self.data[k] += other.data[k]
        return self