import sys
import os

# Thêm thư mục gốc của dự án vào PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import các module từ dự án
from app import map_view, data_input, result_view, control_panel
import streamlit as st

def main():
    # Đặt tiêu đề chính cho ứng dụng
    st.set_page_config(page_title="Water Network Management System", layout="wide")
    st.title("Water Network Management System")

    # Tạo menu điều hướng trong sidebar
    menu = {
        "Map View": "Xem bản đồ và quản lý điểm",
        "Data Input": "Nhập dữ liệu và kết nối",
        "Result View": "Xem kết quả phân tích",
        "Control Panel": "Cài đặt và điều chỉnh hệ thống",
    }
    choice = st.sidebar.selectbox("Chọn trang", list(menu.keys()))

    # Hiển thị mô tả trang trong sidebar
    st.sidebar.markdown(f"**{menu[choice]}**")

    # Điều hướng đến các trang tương ứng
    if choice == "Map View":
        st.sidebar.markdown("---")
        map_view.main()  # Gọi module xử lý bản đồ
    elif choice == "Data Input":
        st.sidebar.markdown("---")
        data_input.show_input_form()  # Gọi module nhập dữ liệu
    elif choice == "Result View":
        st.sidebar.markdown("---")
        result_view.show_results()  # Gọi module hiển thị kết quả
    elif choice == "Control Panel":
        st.sidebar.markdown("---")
        control_panel.show_control_panel()  # Gọi module bảng điều khiển

if __name__ == "__main__":
    main()
