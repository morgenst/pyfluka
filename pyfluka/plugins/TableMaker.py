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
        self.output_dir = "/afs/cern.ch/work/m/morgens/flair++/examples/"
        self.store_multiple_output_files = False
        if 'outputdir' in config:
            self.output_dir = config['outputdir']
            if not os.path.exists(self.output_dir):
                raise IllegalArgumentError("Output directory " + self.output_dir + " does not exist.")
        if 'multipleOutputFiles' in config:
            self.store_multiple_output_files = True
        self.format = 'latex'
        if 'format' in config:
            allowed_format_options = map(str, tabulate.tabulate_formats)
            if config['format'] not in allowed_format_options:
                print 'Invalid formatting option %s. Set to plain' % config['format']
                self.format = 'plain'
            else:
                self.format = config['format']
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
        if not self.store_multiple_output_files:
            f = open(os.path.join(self.output_dir, "tables.tex"), "w")
        for det, table in self.tables.items():
            if self.store_multiple_output_files:
                f = open(os.path.join(self.output_dir, "table_%s.tex" % det), "w")
            print >> f, table
            if self.store_multiple_output_files:
                f.close()
        if not self.store_multiple_output_files:
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
