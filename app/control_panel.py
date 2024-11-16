import streamlit as st
from core.path_finding import find_shortest_path
from core.cost_calculator import calculate_total_cost
from core.report_generator import generate_report

def show_control_panel():
    st.subheader('Control Panel')

    action = st.radio('Choose an action', ['Find Shortest Path', 'Calculate Total Cost', 'Generate Report'])

    if action == 'Find Shortest Path':
        start = st.text_input('Enter start point')
        end = st.text_input('Enter end point')
        if st.button('Find Path'):
            path = find_shortest_path(start, end)
            st.write(f"Shortest Path: {path}")

    elif action == 'Calculate Total Cost':
        total_cost = calculate_total_cost()
        st.write(f"Total Cost of the Network: {total_cost}")

    elif action == 'Generate Report':
        if st.button('Generate Report'):
            generate_report()
            st.success('Report generated successfully!')
