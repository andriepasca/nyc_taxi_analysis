import holoviews as hv
from holoviews import opts, dim
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import seaborn as sns

def chord(dataframe, size):
    hv.extension('bokeh', config=dict(future_deprecations=True))
    hv.output(size=size)
    fig = hv.Chord(dataframe)
    fig.opts(
        opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('level_0').str(), 
                labels='index', node_color=dim('index').str()))
    return hv.render(fig, backend='bokeh')

def clusterplot(labels, x, y):
    g = ox.graph_from_place('New York, USA', network_type='drive')
    fig, ax = ox.plot_graph(g, show=False, close=False, fig_height=16, edge_linewidth=0.1, node_size=1)
    plt.scatter(x, y, s=2, alpha=0.2, zorder=5, c=[np.random.rand(3,) for i in range(len(labels))], label=labels)  
    plt.show()

def route_plotter(location, orig, dest):
    G = ox.graph_from_place(location, network_type='drive')
    route = nx.shortest_path(G, orig, dest)
    fig, ax = ox.plot_graph_route(G, route, route_linewidth=2, node_size=0)
    return fig, ax

def heatmap(dataframe):
    transition_matrix = dataframe.pivot_table(index="pickup", columns="dropoff", values="probability")
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.heatmap(transition_matrix, annot=False, cmap="Blues", fmt=".2f", linewidths=0.5, ax=ax)
    plt.xlabel("To City")
    plt.ylabel("From City")
    ax.set_xticks(range(len(transition_matrix.columns)))
    ax.set_yticks(range(len(transition_matrix.index)))
    ax.set_xticklabels(transition_matrix.columns, rotation=90)
    ax.set_yticklabels(transition_matrix.index, rotation=0)
    return fig

def markov_graph(dataframe):
    G = nx.DiGraph()
    for _, row in dataframe.iterrows():
        G.add_edge(row["pickup"], row["dropoff"], weight=row["probability"])
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", font_size=10)
    edges = G.edges(data=True)
    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    return fig

def route_map(location, origin, destination):
    G = ox.graph_from_place(location, network_type='drive', simplify=True)
    route = nx.shortest_path(G, origin, destination)
    fig, ax = ox.plot_graph_route(G, route, route_linewidth=2, node_size=0)
    return fig
