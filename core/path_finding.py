import networkx as nx
from config.settings import NETWORK_FILE_PATH
import json
import heapq


def load_connections():
    with open(NETWORK_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_shortest_path(start, end):
    connections = load_connections()
    G = nx.Graph()

    for conn in connections['connections']:
        G.add_edge(conn['start'], conn['end'], weight=conn['cost'])

    path = nx.shortest_path(G, source=start, target=end, weight='cost')
    return path


def build_graph(connections):
    graph = {}
    for conn in connections:
        start, end, cost = conn["start"], conn["end"], conn["cost"]
        if start not in graph:
            graph[start] = []
        if end not in graph:
            graph[end] = []
        # Thêm kết nối cho cả hai hướng
        graph[start].append((end, cost))
        graph[end].append((start, cost))
    return graph

# Thuật toán Dijkstra để tìm đường đi ngắn nhất
def dijkstra(graph, start):
    queue = [(0, start)]  # Khởi tạo hàng đợi với điểm gốc và khoảng cách ban đầu là 0
    distances = {start: 0}  # Lưu khoảng cách ngắn nhất tới mỗi đỉnh
    previous_nodes = {start: None}  # Lưu lại cha của mỗi đỉnh để truy vết đường đi
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)  # Lấy node có khoảng cách nhỏ nhất
        
        # Kiểm tra các node hàng xóm
        for neighbor, weight in graph.get(current_node, []):  # Sử dụng graph.get để tránh lỗi KeyError
            distance = current_distance + weight
            
            # Cập nhật khoảng cách nếu tìm thấy đường đi ngắn hơn
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return previous_nodes, distances  # Trả về cha của các node và khoảng cách tới từng điểm
