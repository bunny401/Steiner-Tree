from shapely.geometry import Point
from networkx.utils import pairwise, not_implemented_for
import networkx as nx
import os 
import matplotlib.pyplot as plt
from itertools import combinations, chain


G = nx.Graph()
G.add_node('A=1',pos="1,3!")
G.add_node('B=2',pos="3,1!")
G.add_node('C=3',pos="5,1!")
G.add_node('D=4',pos="3,5!")
G.add_node('E=5',pos="5,5!")
G.add_node('F=6',pos="5,7!")
G.add_node('G=7',pos="7,5!")


G.add_edge('A=1','B=2',weight=1,label='1')
G.add_edge('A=1','C=3',weight=4,label='4')
G.add_edge('B=2','C=3',weight=2,label='2')
G.add_edge('B=2','D=4',weight=3,label='3')
G.add_edge('B=2','E=5',weight=10,label='10')
G.add_edge('C=3','D=4',weight=6,label='6')
G.add_edge('C=3','G=7',weight=3,label='3')
G.add_edge('G=7','D=4',weight=1,label='1')
G.add_edge('G=7','E=5',weight=2,label='2')
G.add_edge('G=7','F=6',weight=5,label='5')
G.add_edge('E=5','D=4',weight=5,label='5')
G.add_edge('E=5','F=6',weight=7,label='7')

p= nx.shortest_path(G, source='A=1',weight='weight')
print('The shortest path from sourc A to destiation B = ',p['B=2'])
print('The shortest path from sourc A to destiation C = ',p['C=3'])
print('The shortest path from sourc A to destiation E = ',p['E=5'])
print('The shortest path from sourc A to destiation G = ',p['G=7'])


M=nx.Graph(G)
M.add_edge(p['B=2'][-1],p['B=2'][-2],color='blue')
M.add_edge(p['C=3'][-1],p['C=3'][-2],color='blue')
M.add_edge(p['E=5'][-1],p['E=5'][-2],color='blue')
M.add_edge(p['G=7'][-1],p['G=7'][-2],color='blue')

def metric_closure(G, weight="weight"):
   
    M = nx.multigraph()

    Gnodes = set(G)

    # check for connected graph while processing first node
    all_paths_iter = nx.all_pairs_dijkstra(G, weight=weight)
    v1, (distance, path) = next(all_paths_iter)
    if Gnodes - set(distance):
        msg = "G is not a connected graph. metric_closure is not defined."
        raise nx.NetworkXError(msg)
        
    Gnodes.remove(v1)
    for v2 in Gnodes:
        M.add_edge(v1, v2, distance=distance[v2], path=path[v2])

    # first node done -- now process the rest
    for v1, (distance, path) in all_paths_iter:
        Gnodes.remove(v1)
        for v2 in Gnodes:
            M.add_edge(v1, v2, distance=distance[v2], path=path[v2])

        Gnodes.remove(v2)
    for v2 in Gnodes:
        M.add_edge(v1, v2, distance=distance[v2], path=path[v2])

    # second node done -- now process the rest
    for v2, (distance, path) in all_paths_iter:
        Gnodes.remove(v2)
        for v3 in Gnodes:
            M.add_edge(v2, v3, distance=distance[v3], path=path[v3])

        Gnodes.remove(v3)
    for v3 in Gnodes:
        M.add_edge(v2, v3, distance=distance[v3], path=path[v3])

    # first node done -- now process the rest
    for v3, (distance, path) in all_paths_iter:
        Gnodes.remove(v3)
        for v4 in Gnodes:
            M.add_edge(v3, v4, distance=distance[v4], path=path[v4])

        Gnodes.remove(v4)
    for v4 in Gnodes:
        M.add_edge(v3, v4, distance=distance[v4], path=path[v4])

    
    return M

def steiner_tree(G, terminal_nodes, weight="weight"):
        
    # H is the subgraph induced by terminal_nodes in the metric closure M of G.
    M = metric_closure(G, weight=weight)
    H = M.subgraph(terminal_nodes)
    # Use the 'distance' attribute of each edge provided by M.
    mst_edges = nx.minimum_spanning_edges(H, weight="distance", data=True)
    # Create an iterator over each edge in each shortest path; repeats are okay
    edges = chain.from_iterable(pairwise(d["path"]) for E, B, d in mst_edges)
    # For multigraph we should add the minimal weight edge keys
    
    if G.is_multigraph():
        edges = (
            (u, v, min(G[u][v], key=lambda k: G[u][v][k][weight])) for u, v in edges
        )
    T = G.edge_subgraph(edges)
    return T



pos=nx.spring_layout(G)
nx.draw(G, pos,with_labels=True, node_size=1200,node_color='blue' )
nx.draw_networkx_edge_labels(G,pos,font_size=14,edge_labels=nx.get_edge_attributes(G,'weight'))

#M= nx.minimum_spanning_tree(M)

plt.show()
#nx.draw(M)

#graph2 = steiner_tree(G, terminal_nodes, weight = 'distance') 

plt.figure()
plt.show()