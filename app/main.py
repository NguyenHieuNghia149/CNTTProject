# main.py

import sys
import os
# Thêm thư mục gốc của dự án vào PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import map_view, data_input, result_view, control_panel
import streamlit as st
import folium
import networkx as nx

def main():
    st.title('Water Network Management System')

    menu = ["Map View", "Data Input", "Result View", "Control Panel"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Map View":
        map_view.show_map()  # Gọi hàm hiển thị bản đồ
    elif choice == "Data Input":
        data_input.show_input_form()
    elif choice == "Result View":
        
        result_view.show_results()
    elif choice == "Control Panel":
        control_panel.show_control_panel()

if __name__ == '__main__':
    main()
