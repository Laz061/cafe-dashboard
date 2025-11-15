import pandas as pd
import streamlit as st
from utils.data_loader import load_cafe_data

# data to show
filepath = 'data/CafeData.csv'
df = load_cafe_data(filepath)

st.set_page_config(layout="wide")
st.title("Cafe Sales Data")

st.header("Raw Data")
st.write(df)