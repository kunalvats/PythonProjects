import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import glob
from cleaning_functions import clean_user_name

def build_graph_from_csvs(path, sep=";,.", num_files=None):
    """
    Given a series of CSVs in the format user1 -> user2
    separated by 'sep', creates a directed graph between
    the users.

    path: the directory holding the csvs
    sep: the separator between users on each line
    num_files: how many files to use from dataset (none defaults to all)
    return graph: networkx graph object
    """
    assert type(path)==str, "Path must be string type"

    if path[-1] == '/':
        path = path[:-1]

    file_list = glob.glob(path+'/*.csv')

    if not num_files:
        num_files = len(file_list)

    graph = nx.DiGraph()

    for file in file_list[:num_files]:
        print("Opening ", file)
        with open(file, 'r') as file_to_be_read:
            for line in file_to_be_read:
                user1, user2 = line.split(sep)
                user1 = clean_user_name(user1)
                user2 = clean_user_name(user2)
                if user1 != "NAN" and user2 != "NAN":
                    graph.add_edge(user1, user2)

    return graph

def draw_di_graph(graph_object, scale_by_degree=True):
    """
    Takes a networkx graph object and draws a plot of the network.

    graph_object: networkx graph object (directional or non)
    scale_by_degree: bool, changes drawn size of nodes to scale
    by number of connections (if True)
    return axis object from matplotlib
    """
    positions = nx.spring_layout(graph_object)
    if scale_by_degree:
        d = nx.degree(graph_object)
        keys, degrees = zip(*d)
        network = nx.draw(graph_object, nodelist=keys,
                          node_size=[5*degree for degree in degrees],
                          pos=positions, alpha=0.5, arrows=False)
    else:
        network = nx.draw(graph_object, pos=positions, node_size=50, alpha=0.5)
    # labels =  nx.draw_networkx_labels(graph, pos=positions)
    return positions, network, plt.gca()

def get_hub_nodes(graph_object, top_n_hubs=10):
    """
    Takes a graph and returns the nodenames for the
    n most connected nodes.

    graph_object: networkx graph object (directional or non)
    top_n_hubs: number of nodenames to return
    return: list of node names and their degrees
    """
    degrees = nx.degree(graph_object)
    sorted_degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
    return sorted_degrees[:top_n_hubs]

def highlight_important_nodes(graph_object, positions, top_n_hubs=10):
    labels = {}
    important_nodes, degrees = zip(*get_hub_nodes(graph_object, top_n_hubs=top_n_hubs))

    for node in graph_object.nodes():
        if node in important_nodes:
            labels[node] = node
    network = nx.draw_networkx_nodes(graph_object, nodelist=labels.values(),
                    node_size=[20 * degree for degree in degrees],
                    pos=positions, node_color='b')
    nx.draw_networkx_labels(important_nodes, positions, labels, font_size=12,
                            font_color='k')