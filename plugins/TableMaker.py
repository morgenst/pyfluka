__author__ = 'marcusmorgenstern'
__mail__ = ''

from utils import PhysicsQuantities as PQ
from base import Calculators as Calcs
from BasePlugin import BasePlugin

class Column:
    def __init__(self, quantity):
        self.quantity = quantity


class TableMaker(BasePlugin):
    def __init__(self, config):
        print config

    def invoke(self):
        pass

    def _writeTable(self, data):
        pass


class LatexTableMaker(TableMaker):
    def __init__(self, config):
        super(self.__class__, self).__init__(config)
        pass