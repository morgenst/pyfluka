__author__ = 'marcusmorgenstern'
__mail__ = ''

from collections import OrderedDict
from tabulate import tabulate
from BasePlugin import BasePlugin
from operator import itemgetter


class Column:
    def __init__(self, quantity):
        self.quantity = quantity

    def __eq__(self, other):
        return (self.quantity == other.quantity)


class TableMaker(BasePlugin):
    def __init__(self, config):
        self.cols = config['cols']

    def invoke(self, data):
        for det, vals in data.items():
            tab = OrderedDict(sorted(filter(lambda c: c[0] in self.cols, vals.iteritems()),
                                     cmp=lambda x, y: self.cols.index(x) - self.cols.index(y),
                                     key=itemgetter(0)))

            """
            work around to stringify
            """
            if 'Isotope' in self.cols:
                tab['Isotope'] = [i.__str__() for i in tab['Isotope']]
            _table = tabulate(tab, tablefmt='latex', floatfmt=".2f")
