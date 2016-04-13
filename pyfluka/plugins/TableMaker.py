__author__ = 'marcusmorgenstern'
__mail__ = ''

import os
from collections import OrderedDict

import numpy as np
import tabulate

from BasePlugin import BasePlugin
from pyfluka.base import InvalidInputError, IllegalArgumentError


class Column:
    def __init__(self, quantity):
        self.quantity = quantity

    def __eq__(self, other):
        return self.quantity == other.quantity


class TableMaker(BasePlugin):
    def __init__(self, config):
        if 'cols' not in config or not len(config['cols']):
            raise InvalidInputError("No columns defined for table. Nothing to do, so giving up.")
        self.cols = config['cols']
        self.tables = OrderedDict()
        self.outputDir = os.path.curdir
        self.storeMultipleOutputFiles = False
        if 'outputdir' in config:
            self.outputDir = config['outputdir']
            if not os.path.exists(self.outputDir):
                raise IllegalArgumentError("Output directory " + self.outputDir + " does not exist.")
        if 'multipleOutputFiles' in config:
            self.storeMultipleOutputFiles = True
        self.__class__._patch_latex_escapes()

    def invoke(self, data):
        self.cols.pop(self.cols.index("Isotope"))
        for det, values in data.items():
            """
            work around to stringify
            """
            isotopes = ["{:L}".format(i)for i in values.keys()]
            values_selected = [map(lambda i: i, elem[self.cols]) for elem in values.values()]
            values_stringified = [map(lambda i: "{:.2eLnune}".format(i), elem[self.cols]) for elem in values.values()]
            values_stringified = self.__class__._transpose(values_stringified)
            headers = self._get_headers(values_selected)
            tab = zip(isotopes, *values_stringified)
            table = tabulate.tabulate(tab, tablefmt='latex', floatfmt=".2f", headers=headers)
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

    def _get_headers(self, values):
        headers = ["Isotope"]
        for col in values[0]:
            header = "{:Lsu}".format(col)
            headers.append(header)
        return headers

    @staticmethod
    def _patch_latex_escapes():
        try:
            del(tabulate.LATEX_ESCAPE_RULES[u'$'])
            del(tabulate.LATEX_ESCAPE_RULES[u'^'])
            del(tabulate.LATEX_ESCAPE_RULES[u'{'])
            del(tabulate.LATEX_ESCAPE_RULES[u'}'])
            del(tabulate.LATEX_ESCAPE_RULES[u'\\'])
        except KeyError:
            pass

    @staticmethod
    def _transpose(l):
        arr = np.array(l)
        return arr.transpose().tolist()
