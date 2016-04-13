__author__ = 'marcusmorgenstern'
__mail__ = ''

import os
import unittest
from collections import OrderedDict
from os.path import join

import pyfluka.base.ConfigParser as CP

import pyfluka.base.GraphBuilder as GB

_basedir = os.path.dirname(__file__)


class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def testBuildGraphSimple(self):
        d = OrderedDict([("A", []), ("B", []), ("C", [])])
        res = ["Input", "A", "B", "C", "Output"]
        graph = GB.build_graph(d)
        self.assertItemsEqual(graph.nodes(), res)

    def testBuildGraphNodesFromYAML(self):
        od = CP.parse(join(_basedir, "test_data/testconfig.yaml"))
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
        path = GB.get_paths(graph)
        self.assertEqual(path.next(), res)

    def test_config_decorate_list(self):
        d = {"A": ["foo", "bar"], "B": [], "C": []}
        res = {"list_config": ["foo", "bar"]}
        graph = GB.build_graph(d)
        self.assertEqual(graph.node["A"], res)

