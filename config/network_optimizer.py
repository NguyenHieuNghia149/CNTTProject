# Các thuật toán tối ưu hóa, ví dụ Dijkstra
import networkx as nx

def optimize_network(connections):
    G = nx.Graph()

    for conn in connections['connections']:
        G.add_edge(conn['start'], conn['end'], weight=conn['cost'])

    return G
