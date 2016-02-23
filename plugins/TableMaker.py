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
        tab = dict(filter(lambda c: c[0] in self.cols, data.iteritems()))
        """
        work around to stringify
        """
        tab['Isotope'] = [i.__str__() for i in tab['Isotope']]
        _table = tabulate(tab, tablefmt='latex', floatfmt=".2f")
        

    def _writeTable(self, data):
        pass

"""
class LatexTableMaker(TableMaker):
    def __init__(self, config):
        super(self.__class__, self).__init__(config)
        pass
"""