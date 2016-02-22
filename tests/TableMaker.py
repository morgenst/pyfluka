__author__ = 'morgenst'

import unittest
from plugins import TableMaker as TM

class ColumnTest(unittest.TestCase):
    def setUp(self):
        pass

    def colInitialisation(self):
        c = TM.Column("ExcemptionLimit")

