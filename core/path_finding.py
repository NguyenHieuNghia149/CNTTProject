import networkx as nx
from config.settings import NETWORK_FILE_PATH
import json
import heapq
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
def find_shortest_path(start, end, connections):
    """
    Tìm đường đi ngắn nhất từ start đến end, bỏ qua các kết nối có status là 'maintenance'.
    """
    # Tạo đồ thị từ danh sách kết nối
    graph = {}
    for conn in connections:
        if conn['status'] == 'active':  # Chỉ xét các kết nối active
            graph.setdefault(conn['start'], []).append((conn['end'], conn['cost']))
            graph.setdefault(conn['end'], []).append((conn['start'], conn['cost']))  # Đồ thị không hướng

    # Dijkstra's algorithm
    pq = [(0, start)]  # (chi phí, điểm bắt đầu)
    distances = {start: 0}  # Khoảng cách từ start đến các điểm
    previous_nodes = {start: None}  # Lưu trữ điểm trước đó để truy vết đường đi
    visited = set()  # Lưu trữ các điểm đã duyệt

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        # Nếu điểm đến được tìm thấy, dừng lại
        if current_node == end:
            break

        for neighbor, cost in graph.get(current_node, []):
            if neighbor in visited:
                continue

            new_distance = current_distance + cost
            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    # Truy vết đường đi từ end đến start
    path = []
    total_cost = distances.get(end, float('inf'))

    if total_cost != float('inf'):
        current_node = end
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]

        path.reverse()  # Đảo ngược để có đúng thứ tự đường đi

    return path, total_cost