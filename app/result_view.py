import streamlit as st
import json
from core.report_generator import *

def load_report():
    with open('data/report/network_report.json', 'r') as f:
        return json.load(f)

def call_report():
    st.subheader('Network Report and Results')

    report = load_report()

    st.write(f"Date: {report['date']}")
    st.write(f"Total Cost: {report['total_cost']}")
    st.write("Network Connections:")
    for conn in report['network_connections']:
        st.write(f"Start: {conn['start']}, End: {conn['end']}, Cost: {conn['cost']}, Status: {conn['status']}")

    st.write("Suggested Connections:")
    for suggestion in report['suggested_connections']:
        st.write(f"Start: {suggestion['start']}, End: {suggestion['end']}, Suggested Cost: {suggestion['suggested_cost']}")
    

def show_results():
    generate_report()
    call_report()