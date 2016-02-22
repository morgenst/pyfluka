__author__ = 'marcusmorgenstern'
__mail__ = ''

import networkx as nx

def build_graph(initList):
    graph = nx.DiGraph()
    graph.add_node("Input")
    graph.add_node("Output")
    previousNode = "Input"
    for key, attr in initList.items():
        graph.add_node(key, attr if isinstance(attr, dict) else {})
        graph.add_edge(previousNode, key)
        previousNode = key
    graph.add_edge(previousNode, "Output")
    return graph

