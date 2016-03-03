__author__ = 'marcusmorgenstern'
__mail__ = ''

import base.GraphBuilder as GB
import unittest
import base.ConfigParser as CP
from collections import OrderedDict


class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def testBuildGraphSimple(self):
        d = OrderedDict([("A", []), ("B", []), ("C", [])])
        res = ["Input", "A", "B", "C", "Output"]
        graph = GB.build_graph(d)
        self.assertItemsEqual(graph.nodes(), res)

    def testBuildGraphNodesFromYAML(self):
        od = CP.parse("testconfig.yaml")
        graph = GB.build_graph(od['plugins'])
        graphRef = ["Input", "AoverLECalculator", "TableMaker", "Output"]
        self.assertItemsEqual(graph.nodes(), graphRef)

    def testEdgesSimple(self):
        d = OrderedDict([("A", None), ("B", None), ("C", None)])
        res = [("Input", "A"), ("A", "B"), ("B", "C"), ("C", "Output")]
        graph = GB.build_graph(d)
        self.assertItemsEqual(graph.edges(), res)

    def testConfigDecorate(self):
        d = {"A": {"foo": "bar"}, "B": [], "C": []}
        res = {"foo": "bar"}
        graph = GB.build_graph(d)
        self.assertEqual(graph.node["A"], res)

    def testPathCreation(self):
        d = OrderedDict([("A", None), ("B", None), ("C", None)])
        res = ["Input", "A", "B", "C", "Output"]
        graph = GB.build_graph(d)
        path = GB.getPaths(graph)
        self.assertEqual(path.next(), res)