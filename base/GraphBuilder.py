__author__ = 'marcusmorgenstern'
__mail__ = ''

import networkx as nx


def build_graph(init_list):
    """
    Builds path of plugins to be analysed
    :param init_list (list): list of plugins in order of execution
    :return (networkx.DiGraph): full analysis graph
    """
    graph = nx.DiGraph()
    graph.add_node("Input")
    graph.add_node("Output")
    previous_node = "Input"
    for key, attr in init_list.items():
        if isinstance(attr, list):
            attr = {"list_config": attr}
        graph.add_node(key, attr if isinstance(attr, dict) else {})
        graph.add_edge(previous_node, key)
        previous_node = key
    graph.add_edge(previous_node, "Output")
    return graph


def get_paths(graph):
    """
    Determines all possible paths between input and output node
    :param graph (networkx.DiGraph): graph to be analysed
    :return: list of all paths b/w input and output note for given path
    """
    return nx.algorithms.all_simple_paths(graph, "Input", "Output")

