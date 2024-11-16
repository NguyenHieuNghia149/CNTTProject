import folium
from streamlit_folium import folium_static
import streamlit as st
import json
import os

# Đọc tọa độ từ file JSON
def read_coordinates():
    coordinates_file = 'data/coordinates.json'
    if os.path.exists(coordinates_file):
        with open(coordinates_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
            if isinstance(data, list):
                return data
            # Nếu dữ liệu là dict, cố gắng lấy 'connections'
            return data.get('coordinates', [])
    return []

# Đọc các kết nối từ file JSON
def read_connections():
    connections_file = 'data/connections.json'
    if os.path.exists(connections_file):
        with open(connections_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Nếu dữ liệu là danh sách, trả về trực tiếp
            if isinstance(data, list):
                return data
            # Nếu dữ liệu là dict, cố gắng lấy 'connections'
            return data.get('connections', [])
    return []

# Lấy tọa độ của điểm theo tên từ coordinates.json
def get_coordinates_by_name(name, coordinates):
    for coord in coordinates:
        if coord["name"] == name:
            return coord["coordinates"]
    return None

# Hàm thêm marker vào bản đồ
def add_marker(map_obj, coordinates, popup_text):
    if isinstance(coordinates, (list, tuple)) and len(coordinates) == 2:
        folium.Marker(coordinates, popup=popup_text).add_to(map_obj)
    else:
        st.error(f"Invalid coordinates: {coordinates}")

# Hàm vẽ đường nối giữa hai điểm
def draw_connection(map_obj, coord_from, coord_to, cost, status):
    line = folium.PolyLine([coord_from, coord_to], color="blue", weight=2.5, opacity=1)
    line.add_to(map_obj)
    # Thêm thông tin chi phí và trạng thái vào popup của đường nối
    line_popup = f"Cost: {cost} | Status: {status}"
    folium.Popup(line_popup).add_to(line)

# Hiển thị bản đồ và các marker từ tọa độ trong file JSON
def show_map():
    # Tạo bản đồ
    m = folium.Map(location=[10.850923620459348, 106.76728506920097], zoom_start=12)

    # Đọc các tọa độ đã lưu từ file
    coordinates = read_coordinates()

    # Đọc các kết nối đã lưu từ file
    connections = read_connections()

    # Thêm các marker cho mỗi tọa độ đã lưu
    for coord in coordinates:
        add_marker(m, coord["coordinates"], f'{coord["name"]}')

    # Vẽ các tuyến đường nối giữa các điểm dựa trên kết nối
    for conn in connections:
        # Lấy tọa độ từ coordinates.json
        coord_from = get_coordinates_by_name(conn["start"], coordinates)
        coord_to = get_coordinates_by_name(conn["end"], coordinates)
        
        if coord_from and coord_to:
            # Kiểm tra xem tọa độ có hợp lệ không trước khi vẽ đường nối
            draw_connection(m, coord_from, coord_to, conn["cost"], conn["status"])

    # Hiển thị bản đồ trong Streamlit
    folium_static(m)
