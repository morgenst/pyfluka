__author__ = 'marcusmorgenstern'
__mail__ = ''

import os
from base import InvalidInputError, IllegalArgumentError
from collections import OrderedDict
from tabulate import tabulate
from BasePlugin import BasePlugin
from operator import itemgetter


class Column:
    def __init__(self, quantity):
        self.quantity = quantity

    def __eq__(self, other):
        return self.quantity == other.quantity


class TableMaker(BasePlugin):
    def __init__(self, config):
        if not config.has_key('cols') or not len(config['cols']):
            raise InvalidInputError("No colums defined for table. Nothing to do, so giving up.")
        self.cols = config['cols']
        self.tables = OrderedDict()
        self.outputDir = os.path.curdir
        self.storeMultipleOutputFiles = False
        if config.has_key('outputdir'):
            self.outputDir = config['outputdir']
            if not os.path.exists(self.outputDir):
                raise IllegalArgumentError("Output directory " + self.outputDir + " does not exist.")
        if config.has_key('multipleOutputFiles'):
            self.storeMultipleOutputFiles = True

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
            table = tabulate(tab, tablefmt='latex', floatfmt=".2f")
            self.tables[det] = table
        self.store()

    def store(self):
        f = None
        if not self.storeMultipleOutputFiles:
            f = open(os.path.join(self.outputDir, "tables.tex"), "w")
        for det, table in self.tables.items():
            if self.storeMultipleOutputFiles:
                f = open(os.path.join(self.outputDir, "table_%s.tex" % det), "w")
            print >> f, table
            if self.storeMultipleOutputFiles:
                f.close()
        if not self.storeMultipleOutputFiles:
            f.close()


