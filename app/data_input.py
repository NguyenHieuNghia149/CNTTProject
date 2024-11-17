import streamlit as st
import json

# Hàm load danh sách địa điểm
def load_coordinates():
    with open('data/coordinates.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Hàm load danh sách kết nối
def load_connections():
    try:
        with open('data/connections.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Nếu file không tồn tại, trả về danh sách rỗng

# Hàm hiển thị form nhập liệu
def show_input_form():
    st.subheader('Data Input - Add/Update Connections')

    # Load danh sách địa điểm và kết nối
    coordinates = load_coordinates()
    connections = load_connections()

    # Danh sách các điểm bắt đầu và kết thúc
    points = [location['name'] for location in coordinates]
    start_points = points  # Điểm bắt đầu
    end_points = points  # Điểm kết thúc

    # Cho phép người dùng thêm kết nối mới
    start_point = st.selectbox('Select start point', start_points)
    end_point = st.selectbox('Select end point', end_points)
    cost = st.number_input('Cost of connection', min_value=0)
    status = st.selectbox('Connection status', ['active', 'maintenance'])

    if st.button('Add Connection'):
        new_connection = {
            "start": start_point,
            "end": end_point,
            "cost": cost,
            "status": status
        }
        # Thêm kết nối mới vào danh sách
        connections.append(new_connection)
        # Ghi lại danh sách vào tệp JSON
        with open('data/connections.json', 'w', encoding='utf-8') as f:
            json.dump(connections, f, indent=4, ensure_ascii=False)
        st.success('Connection added successfully!')