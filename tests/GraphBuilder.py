__author__ = 'marcusmorgenstern'
__mail__ = ''

import base.GraphBuilder as GB
import unittest
import base.ConfigParser as CP
from collections import OrderedDict


class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def testSimplePath(self):
        graph = {"A" : ["B"]}
        res = ["A", "B"]
        path = GB.build_path(graph, "A", "B")
        self.assertEqual(path, res)

    def testComplexPath(self):
        graph = {"A" : ["B", "C"],
                 "B" : ["C", "D"]}
        res = ["A", "B", "D"]
        path = GB.build_path(graph, "A", "D")
        self.assertEqual(path, res)

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
