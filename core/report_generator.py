import json
from datetime import datetime
from config.settings import REPORT_FILE_PATH, NETWORK_FILE_PATH

def generate_report():
    # Step 1: Load connections from connection.json
    try:
        with open(NETWORK_FILE_PATH, 'r', encoding='utf-8') as conn_file:
            connections = json.load(conn_file)
    except FileNotFoundError:
        print("Error: connection.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: connection.json contains invalid JSON.")
        return

    # Step 2: Prepare the report data
    network_connections = []
    for conn in connections:
        if isinstance(conn, dict):  # Ensure the connection is a dictionary
            network_connections.append({
                "start": conn.get("start", "Unknown"),
                "end": conn.get("end", "Unknown"),
                "cost": conn.get("cost", 0),
                "status": conn.get("status", "unknown")
            })
        else:
            print(f"Invalid connection entry skipped: {conn}")

   

    report = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_cost": sum(conn.get("cost", 0) for conn in network_connections),
        "network_connections": network_connections,
    }

    # Step 3: Write the report to network_report.json
    try:
        with open(REPORT_FILE_PATH, 'w', encoding='utf-8') as report_file:
            json.dump(report, report_file, indent=4)
        print("Report generated successfully.")
    except Exception as e:
        print(f"Error writing the report: {e}")
