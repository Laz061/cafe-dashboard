import pandas as pd
import streamlit as st

df = pd.read_csv('data/CafeData.csv')

st.set_page_config(layout="wide")
st.title("Cafe Sales Data")

st.header("Raw Data")
st.write(df)