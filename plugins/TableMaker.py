__author__ = 'marcusmorgenstern'
__mail__ = ''

from tabulate import tabulate
from utils import PhysicsQuantities as PQ
from base import Calculators as Calcs
from BasePlugin import BasePlugin

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
            tab = dict(filter(lambda c: c[0] in self.cols, vals.iteritems()))
            """
            work around to stringify
            """
            if 'Isotope' in self.cols:
                tab['Isotope'] = [i.__str__() for i in tab['Isotope']]
            _table = tabulate(tab, tablefmt='latex', floatfmt=".2f")
            print _table

    def _writeTable(self, data):
        pass
