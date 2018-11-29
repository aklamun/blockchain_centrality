# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 20:21:57 2018

This was an exploratory mini-project to look at centrality rating of blockchain transaction graphs. The idea was to try to learn about creditworthiness (more specifically, willingness to transact with) of entities in these graphs. The main problem is that an adversary can generate transactions that easily game the usual network analysis tools. This is relevant for tools such as nebulas.io

The code uses transaction data from the ELTE Bitcoin Project, available at http://www.vo.elte.hu/bitcoin/downloads.htm

@author: ariahKlages-Mundt
"""

import networkx as nx
import operator

G = nx.MultiDiGraph()
f = open('bitcoin_graphs/graphs_njp/au_graph.txt')
for line in f:
    node1,node2,time = line.split('\t')
    node1,node2 = [int(node1),int(node2)]
    if node1 != node2:
        G.add_edge(node1,node2)
f.close()
del f

source = 0
G.add_node(source)
for node in G.nodes():
    G.add_edge(source,node)
    G.add_edge(node,source)

#nx.node_connectivity(G) #if 0 then graph is disconnected, need to use source node method
eig_centrality = nx.algorithms.centrality.eigenvector_centrality_numpy(G)
max_ind = max(eig_centrality.items(), key=operator.itemgetter(1))[0]
min_ind = min(eig_centrality.items(), key=operator.itemgetter(1))[0]
pagerank = nx.pagerank_scipy(G)
pprank_dict0 = {}
for node in G.nodes():
    pprank_dict0[node] = 0
pprank_dict0[list(G.nodes())[0]]=1
pprank = nx.pagerank_scipy(G,personalization=pprank_dict0)

#demonstrate that adding cycles of transactions can artificially boost centrality score
H = G.copy()
for i in range(100):
    H.add_edge(max_ind, min_ind)
    H.add_edge(min_ind, max_ind)
eig_centrality_H = nx.algorithms.centrality.eigenvector_centrality_numpy(H)
print(eig_centrality_H[min_ind]/eig_centrality[min_ind])


G2 = nx.DiGraph(G)
out_degs = G2.out_degree()
edges = G2.edges()
for edge in edges:
    start = edge[0]
    end = edge[1]
    wt = 1/out_degs[start]
    G2.add_edge(start,end,weight=wt)
eig_centrality_G2 = nx.algorithms.centrality.eigenvector_centrality_numpy(G2)

G3 = nx.MultiDiGraph()
G3.add_nodes_from(G.nodes())
out_degs = G.out_degree()
edges = G.edges()
for edge in edges:
    start = edge[0]
    end = edge[1]
    wt = 1/out_degs[start]
    G3.add_edge(start,end,weight=wt)
eig_centrality_G3 = nx.algorithms.centrality.eigenvector_centrality_numpy(G3)
