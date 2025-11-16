import pandas as pd
import streamlit as st
from utils.data_loader import load_cafe_data
from utils.revenue import display_revenue_section
from utils.feedback import display_feedback_section
from utils.analysis import display_ai_section

# data to show
filepath = 'data/CafeData.csv'
data = load_cafe_data(filepath)

st.set_page_config(layout="wide")

st.title("☕ Cafe Sales Dashboard")

with st.sidebar:
    display_ai_section(data)
display_revenue_section(data)
display_feedback_section(data)


st.header("Raw Data")
st.write(data)