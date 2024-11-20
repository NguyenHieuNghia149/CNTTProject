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
    return []

# Đọc các kết nối từ file JSON
def read_connections():
    connections_file = 'data/connections.json'
    if os.path.exists(connections_file):
        with open(connections_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):  # Nếu là danh sách, trả về trực tiếp
                return data
            return data.get('connections', [])  # Nếu là dict, trả về 'connections'
    return []

# Lấy tọa độ của điểm theo tên từ coordinates.json
def get_coordinates_by_name(name, coordinates):
    for coord in coordinates:
        if coord["name"] == name:
            return coord["coordinates"]
    return None

# Hàm vẽ đường nối giữa hai điểm
def draw_connection(map_obj, coord_from, coord_to, cost, status):
    line = folium.PolyLine(
        [coord_from, coord_to],
        color="blue" if status == "active" else "red",  # Đổi màu theo trạng thái
        weight=2.5,
        opacity=1
    )
    line_popup = f"Cost: {cost} | Status: {status}"
    folium.Popup(line_popup).add_to(line)
    line.add_to(map_obj)

# Lưu tọa độ vào file JSON
def save_coordinates(coordinates):
    coordinates_file = 'data/coordinates.json'
    with open(coordinates_file, 'w', encoding='utf-8') as f:
        json.dump(coordinates, f, ensure_ascii=False, indent=4)

# Lưu các kết nối vào file JSON
def save_connections(connections):
    connections_file = 'data/connections.json'
    with open(connections_file, 'w', encoding='utf-8') as f:
        json.dump(connections, f, ensure_ascii=False, indent=4)

# Thêm marker vào bản đồ
def add_marker(map_obj, coordinates, popup_text):
    if isinstance(coordinates, (list, tuple)) and len(coordinates) == 2:
        folium.Marker(coordinates, popup=popup_text).add_to(map_obj)
    else:
        st.error(f"Invalid coordinates: {coordinates}")

# Hiển thị bản đồ và các marker từ tọa độ trong file JSON
def show_map():
    # Tạo bản đồ
    m = folium.Map(location=[10.85047074597321, 106.77195312611487], zoom_start=12)

    # Đọc các tọa độ đã lưu từ file
    coordinates = read_coordinates()

    # Đọc các kết nối đã lưu từ file
    connections = read_connections()

    # Tập hợp tất cả các tọa độ để tính bounding box
    bounds = []

    # Thêm các marker cho mỗi tọa độ đã lưu
    for coord in coordinates:
        add_marker(m, coord["coordinates"], f'{coord["name"]}')
        bounds.append(coord["coordinates"])  # Lưu lại tọa độ để fit bounds

    # Vẽ các tuyến đường nối giữa các điểm dựa trên kết nối
    for conn in connections:
        coord_from = get_coordinates_by_name(conn["start"], coordinates)
        coord_to = get_coordinates_by_name(conn["end"], coordinates)
        if coord_from and coord_to:
            draw_connection(m, coord_from, coord_to, conn["cost"], conn["status"])
            bounds.extend([coord_from, coord_to])  # Thêm tọa độ vào bounds

    # Điều chỉnh bản đồ để hiển thị tất cả các điểm
    if bounds:
        m.fit_bounds(bounds)

    # Hiển thị bản đồ trong Streamlit
    folium_static(m)

# Thêm ô nhập tọa độ mới
def add_new_coordinate():
    st.markdown("<h3 style='font-weight: bold; font-size: 24px;'>Add new coordinates</h3>", unsafe_allow_html=True)
    name = st.text_input("Name:")
    lat = st.number_input("Latitude:", min_value=-90.0, max_value=90.0, format="%.6f")
    lon = st.number_input("Longitude:", min_value=-180.0, max_value=180.0, format="%.6f")

    if st.button("Add"):
        if name and lat and lon:
            coordinates = read_coordinates()
            new_coordinate = {"name": name, "coordinates": [lat, lon]}
            coordinates.append(new_coordinate)
            save_coordinates(coordinates)
            st.success("New coordinates have been added successfully!")
            st.experimental_rerun()
        else:
            st.error("Vui lòng nhập đủ thông tin.")

# Xóa tọa độ khỏi files JSON
def delete_coordinate(selected_name):
    coordinates = read_coordinates()
    connections = read_connections()

    # Xóa điểm khỏi coordinates.json
    coordinates = [coord for coord in coordinates if coord["name"] != selected_name]
    save_coordinates(coordinates)

    # Xóa tất cả kết nối liên quan khỏi connections.json
    connections = [conn for conn in connections if conn["start"] != selected_name and conn["end"] != selected_name]
    save_connections(connections)

    st.success(f"Đã xóa điểm '{selected_name}' thành công.")
    st.experimental_rerun()

# Hiển thị danh sách các điểm và cho phép xóa
def delete_existing_coordinate():
    st.markdown("<h3 style='font-weight: bold; font-size: 24px;'>Delete coordinates</h3>", unsafe_allow_html=True)
    coordinates = read_coordinates()
    names = [coord["name"] for coord in coordinates]
    selected_name = st.selectbox("Select coordinates to delete:", options=["-- Chọn điểm --"] + names)

    if st.button("Delete"):
        if selected_name and selected_name != "-- Chọn điểm --":
            delete_coordinate(selected_name)
        else:
            st.error("Vui lòng chọn điểm hợp lệ để xóa.")

# Gọi các hàm trong Streamlit để hiển thị bản đồ và ô nhập/xóa tọa độ mới
def main():
    st.title("Coordinate map")
    col1, col2 = st.columns([3, 1])

    with col1:
        show_map()

    with st.sidebar:
        add_new_coordinate()
        st.markdown("<hr>", unsafe_allow_html=True)
        delete_existing_coordinate()

if __name__ == "__main__":
    main()
