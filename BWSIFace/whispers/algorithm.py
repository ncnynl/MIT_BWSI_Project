# from node import Node
# from ..profile import Profile

import networkx as nx
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt


def run(nodes):
    changed = True
    pres = []
    recs = []
    while changed:
        changed = False
        # print("iteration", flush = True)
        for i, node in enumerate(nodes):
            neighbors = node.neighbors
            count = {}
            for key in neighbors:
                curNode = key
                if curNode.label in count:
                    count[curNode.label] +=neighbors[key]
                else:
                    count[curNode.label] = neighbors[key]
            maxVal = -1
            maxKey = None
            for key in count:
                if(count[key]>maxVal):
                    maxVal = count[key]
                    maxKey = key
            if node.label !=maxKey:
                changed = True
            node.label = maxKey
            # print("Label: {}".format(node.label))
        precision, recall = pairwise(nodes)
        pres.append(precision)
        recs.append(recall)
    return (pres, recs)

def plot_graph(graph, adj, labels):
    """ Use the package networkx to produce a diagrammatic plot of the graph, with
        the nodes in the graph colored according to their current labels.

        Note that only 20 unique colors are available for the current color map,
        so common colors across nodes may be coincidental.

        Parameters
        ----------
        graph : Tuple[Node, ...]
            The graph to plot
            
        adj : numpy.ndarray, shape=(N, N)
            The adjacency-matrix for the graph. Nonzero entries indicate
            the presence of edges.

        Returns
        -------
        Tuple[matplotlib.fig.Fig, matplotlib.axis.Axes]
            The figure and axes for the plot."""

    g = nx.Graph()
    for n, node in enumerate(graph):
        g.add_node(n)

    g.add_edges_from(zip(*np.where(np.triu(adj) > 0)))
    pos = nx.spring_layout(g)

    color = list(iter(cm.Vega20b(np.linspace(0, 1, len(set(i.label for i in graph))))))
    color_map = dict(zip(sorted(set(i.label for i in graph)), color))
    colors = [color_map[i.label] for i in graph]
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(g, pos=pos, ax=ax, nodelist=range(len(graph)), node_color=colors)
    nx.draw_networkx_edges(g, pos, ax=ax, edgelist=g.edges())
    nx.draw_networkx_labels(g,pos = pos, ax = ax, labels = labels)
    return fig, ax


def generate_adj(nodes):
    adj = np.zeros((len(nodes), len(nodes)))
    labels = {}
    for i, node in enumerate(nodes):
        labels[node.id] = node.data.name[0]
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if node2 in node1.neighbors:
                adj[i, j] = node1.neighbors[node2]
                adj[j, i] = node1.neighbors[node2]
    return (adj, labels)

def pairwise(nodes):
    #      labels    truth
    mm = 0 #match    match
    md = 0 #match    disagree
    dm = 0 #disagree match
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if i==j: continue
            if node1.label == node2.label and node1.truth == node2.truth:
                mm +=1
            elif node1.label == node2.label and node1.truth != node2.truth:
                md+=1
            elif node1.label != node2.label and node1.truth == node2.truth:
                dm+=1
    precision = mm/(mm+dm)
    recall = mm/(mm+md)
    return (precision, recall)