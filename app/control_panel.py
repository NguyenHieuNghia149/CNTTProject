import streamlit as st
import json
import folium
from streamlit_folium import st_folium
from core.path_finding import find_shortest_path
from core.report_generator import generate_report
from datetime import datetime

# Hàm load dữ liệu từ connections.json
def load_connections():
    try:
        with open('data/connections.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("File 'connections.json' not found!")
        return []
    except json.JSONDecodeError:
        st.error("File 'connections.json' is not a valid JSON!")
        return []

# Hàm load dữ liệu từ coordinates.json
def load_coordinates():
    try:
        with open('data/coordinates.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {entry['name']: entry['coordinates'] for entry in data}
    except FileNotFoundError:
        st.error("File 'coordinates.json' not found!")
        return {}
    except json.JSONDecodeError:
        st.error("File 'coordinates.json' is not a valid JSON!")
        return {}

# Hàm tạo bản đồ
def create_map(path, coordinates, connections):
    center = [10.852960874075226, 106.77441278660831]
    m = folium.Map(location=center, zoom_start=16)

    # Vẽ tất cả các đường trong connections.json
    for conn in connections:
        start = conn['start']
        end = conn['end']
        if start in coordinates and end in coordinates:
            folium.PolyLine(
                locations=[coordinates[start], coordinates[end]],
                color='blue',
                weight=2,
                opacity=0.6,
                tooltip=f"{start} -> {end}"
            ).add_to(m)

    # Vẽ đường đi ngắn nhất nếu có
    if path:
        path_coords = [coordinates[node] for node in path if node in coordinates]
        folium.PolyLine(
            locations=path_coords,
            color='red',
            weight=4,
            opacity=1,
            tooltip="Shortest Path"
        ).add_to(m)

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

    default_start = "Nhà máy nước Thủ Đức" if "Nhà máy nước Thủ Đức" in start_points else start_points[0]

    # Lựa chọn hành động
    action = st.radio('Choose an action', ['Find Shortest Path', 'Generate Report'])

    if action == 'Find Shortest Path':
        start = st.selectbox('Select start point', start_points, index=start_points.index(default_start))
        end = st.selectbox('Select end point', end_points)

        if st.button('Find Path'):
            if start not in coordinates or end not in coordinates:
                st.error("Selected points are invalid or missing coordinates!")
            else:
                path, total_cost = find_shortest_path(start, end, connections)
                st.session_state['path'] = path
                st.session_state['total_cost'] = total_cost

        if 'path' in st.session_state and st.session_state['path']:
            path = st.session_state['path']
            total_cost = st.session_state['total_cost']
            st.success(f"Shortest Path: {' -> '.join(path)}")
            st.info(f"Total Cost: {total_cost}")

            map_object = create_map(path, coordinates, connections)
            st_folium(map_object, width=700, height=500)

    elif action == 'Generate Report':  # Đã thụt lề đúng ở đây
        if st.button('Generate Report'):
            if 'path' not in st.session_state or not st.session_state['path']:
                st.warning("Please calculate the shortest path first!")
            else:
                # Tạo nội dung báo cáo
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                path = st.session_state['path']
                total_cost = st.session_state['total_cost']
                report_content = f"""Water Network Management System - Report
=======================================
Generated on: {timestamp}
Shortest Path: {' -> '.join(path)}
Total Cost: {total_cost}
=======================================
"""

                # Lưu báo cáo vào session_state để không bị mất
                st.session_state['report_content'] = report_content

                st.success('Report generated successfully!')

        # Hiển thị nút tải báo cáo nếu báo cáo đã được tạo
        if 'report_content' in st.session_state:
            try:
                with open("water_network_report.txt", "w", encoding="utf-8") as f:
                    f.write(st.session_state['report_content'])

                with open("water_network_report.txt", "r", encoding="utf-8") as f:
                    st.download_button(
                        label="Download Report",
                        data=f,
                        file_name="water_network_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"Error generating report: {e}")

# Gọi hàm hiển thị giao diện
if __name__ == '__main__':
    st.title("Water Network Management System")
    show_control_panel()
