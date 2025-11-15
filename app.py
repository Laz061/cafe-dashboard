import pandas as pd
import streamlit as st
from utils.data_loader import load_cafe_data

# data to show
filepath = 'data/CafeData.csv'
data = load_cafe_data(filepath)

st.set_page_config(layout="wide")
st.title("Cafe Sales Dashboard")

# Calculate the cutoff date for the last two years
cutoff_date = pd.to_datetime('today') - pd.DateOffset(years=2)

# Filter data for the chart
chart_data = data[data['TransactionDateTime'] >= cutoff_date].sort_values('TransactionDateTime')

# --- Daily Revenue Chart ---
st.header("Total Daily Revenue (Last 2 Years)")
# To get daily totals, set the datetime as the index and resample by day ('D')
daily_revenue = chart_data.set_index('TransactionDateTime').resample('D')['TransactionValue'].sum()
st.line_chart(daily_revenue)


st.header("Raw Data")
st.write(data)