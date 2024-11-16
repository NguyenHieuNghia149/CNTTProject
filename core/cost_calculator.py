import json
from config.settings import NETWORK_FILE_PATH

def calculate_total_cost():
    with open(NETWORK_FILE_PATH, 'r', encoding='utf-8') as f:
        connections = json.load(f)

    total_cost = sum(conn['cost'] for conn in connections['connections'])
    return total_cost
