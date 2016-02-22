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


def build_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = build_path(graph, node, end, path)
            if newpath: return newpath
    return None