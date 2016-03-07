__author__ = 'marcusmorgenstern'
__mail__ = ''

import networkx as nx


def build_graph(init_list):
    graph = nx.DiGraph()
    graph.add_node("Input")
    graph.add_node("Output")
    previous_node = "Input"
    for key, attr in init_list.items():
        graph.add_node(key, attr if isinstance(attr, dict) else {})
        graph.add_edge(previous_node, key)
        previous_node = key
    graph.add_edge(previous_node, "Output")
    return graph


def get_paths(graph):
    return nx.algorithms.all_simple_paths(graph, "Input", "Output")

