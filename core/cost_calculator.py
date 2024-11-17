import json
from config.settings import NETWORK_FILE_PATH  # Đảm bảo rằng đường dẫn này đúng

def load_connections():
    try:
        with open(NETWORK_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Nếu file không tồn tại, trả về danh sách rỗng

def calculate_total_cost():
    # Load dữ liệu kết nối
    connections = load_connections()

    # Tính tổng chi phí của tất cả các kết nối
    total_cost = sum(conn['cost'] for conn in connections)
    return total_cost
