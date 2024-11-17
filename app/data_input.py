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

# Hàm lưu danh sách kết nối
def save_connections(connections):
    with open('data/connections.json', 'w', encoding='utf-8') as f:
        json.dump(connections, f, indent=4, ensure_ascii=False)

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

    # Cho phép người dùng thêm hoặc chỉnh sửa kết nối
    start_point = st.selectbox('Select start point', start_points)
    end_point = st.selectbox('Select end point', end_points)
    cost = st.number_input('Cost of connection', min_value=0)
    status = st.selectbox('Connection status', ['active', 'maintenance'])

    if st.button('Add/Update Connection'):
        # Kiểm tra nếu kết nối đã tồn tại
        updated = False
        for connection in connections:
            if connection['start'] == start_point and connection['end'] == end_point:
                # Cập nhật thông tin nếu tồn tại
                connection['cost'] = cost
                connection['status'] = status
                updated = True
                break
        
        if not updated:
            # Thêm kết nối mới nếu chưa tồn tại
            new_connection = {
                "start": start_point,
                "end": end_point,
                "cost": cost,
                "status": status
            }
            connections.append(new_connection)
        
        # Lưu danh sách kết nối
        save_connections(connections)
        
        if updated:
            st.success('Connection updated successfully!')
        else:
            st.success('Connection added successfully!')

