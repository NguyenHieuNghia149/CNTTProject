import streamlit as st
import json
import folium
from streamlit_folium import st_folium
from core.path_finding import find_shortest_path
from core.cost_calculator import calculate_total_cost
from core.report_generator import generate_report

# Hàm load dữ liệu từ connections.json
def load_connections():
    try:
        with open('data/connections.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Nếu file không tồn tại, trả về danh sách rỗng

# Hàm load dữ liệu từ coordinates.json
def load_coordinates():
    try:
        with open('data/coordinates.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Chuyển đổi dữ liệu thành dictionary {name: coordinates}
            return {entry['name']: entry['coordinates'] for entry in data}
    except FileNotFoundError:
        st.error("File 'coordinates.json' not found!")
        return {}
    except json.JSONDecodeError:
        st.error("File 'coordinates.json' is not a valid JSON!")
        return {}

# Hàm tạo bản đồ
def create_map(path, coordinates, connections):
    """
    Tạo bản đồ hiển thị tất cả các điểm và đường kết nối trong connections.json.
    Đường ngắn nhất được tìm thấy sẽ được đánh dấu khác màu.
    """
    # Tạo bản đồ trung tâm
    center = [10.852960874075226, 106.77441278660831]
    m = folium.Map(location=center, zoom_start=16)

    # Vẽ tất cả các đường trong connections.json
    for conn in connections:
        start = conn['start']
        end = conn['end']
        if start in coordinates and end in coordinates:
            folium.PolyLine(
                locations=[coordinates[start], coordinates[end]],
                color='blue',  # Màu mặc định cho các đường
                weight=2,
                opacity=0.6,
                tooltip=f"{start} -> {end}"
            ).add_to(m)

    # Vẽ đường đi ngắn nhất nếu có
    if path:
        path_coords = [coordinates[node] for node in path if node in coordinates]
        folium.PolyLine(
            locations=path_coords,
            color='red',  # Màu khác cho đường ngắn nhất
            weight=4,
            opacity=1,
            tooltip="Shortest Path"
        ).add_to(m)

        # Đánh dấu các điểm trên đường đi ngắn nhất
        for idx, coord in enumerate(path_coords):
            folium.Marker(
                location=coord,
                popup=f"{path[idx]}",
                icon=folium.Icon(color="blue" if idx == 0 else "green" if idx == len(path_coords) - 1 else "orange")
            ).add_to(m)

    return m

# Hàm hiển thị giao diện
def show_control_panel():
    st.subheader('Control Panel')

    # Load danh sách kết nối và tọa độ
    connections = load_connections()
    coordinates = load_coordinates()

    if not connections or not coordinates:
        st.error("Connections or coordinates data is missing!")
        return

    # Lấy danh sách các điểm bắt đầu và kết thúc
    start_points = list(set(conn['start'] for conn in connections))
    end_points = list(set(conn['end'] for conn in connections))

    # Mặc định điểm bắt đầu
    default_start = "Nhà máy nước Thủ Đức" if "Nhà máy nước Thủ Đức" in start_points else start_points[0]

    # Chọn hành động
    action = st.radio('Choose an action', ['Find Shortest Path', 'Calculate Total Cost', 'Generate Report'])

    if action == 'Find Shortest Path':
        # Selectbox cho điểm bắt đầu và kết thúc
        start = st.selectbox('Select start point', start_points, index=start_points.index(default_start))
        end = st.selectbox('Select end point', end_points)

        # Lưu trạng thái khi nhấn nút
        if st.button('Find Path'):
            path, total_cost = find_shortest_path(start, end, connections)
            st.session_state['path'] = path
            st.session_state['total_cost'] = total_cost

        # Hiển thị kết quả nếu đã tìm được
        if 'path' in st.session_state and st.session_state['path']:
            path = st.session_state['path']
            total_cost = st.session_state['total_cost']
            st.write(f"Shortest Path: {' -> '.join(path)}")
            st.write(f"Total Cost: {total_cost}")

            # Tạo bản đồ với đường ngắn nhất
            map_object = create_map(path, coordinates, connections)
            st_folium(map_object, width=700, height=500)

    elif action == 'Calculate Total Cost':
        total_cost = calculate_total_cost()
        st.write(f"Total Cost of the Network: {total_cost}")

    elif action == 'Generate Report':
        if st.button('Generate Report'):
            generate_report()
            st.success('Report generated successfully!')

    # Hiển thị bản đồ tất cả các đường và điểm nếu không chọn gì
    if action != 'Find Shortest Path':
        map_object = create_map(None, coordinates, connections)
        st_folium(map_object, width=700, height=500)

# Gọi hàm hiển thị giao diện
if __name__ == '__main__':
    st.title("Water Network Management System")
    show_control_panel()
