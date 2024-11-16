import streamlit as st
import json
from config import *

def load_connections():
    with open('data/connections.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def show_input_form():
    st.subheader('Data Input - Add/Update Connections')

    connections = load_connections()  # Load the list of connections

    # Danh sách các điểm bắt đầu và kết thúc hiện có
    start_points = list(set(conn['start'] for conn in connections))
    end_points = list(set(conn['end'] for conn in connections))

    # Allow user to add new connections
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

