import streamlit as st
import pandas as pd

def display_revenue_section(df):
    """
    Calculates and displays a line chart of total daily revenue for the last years.

    Args:
        df (pd.DataFrame): The input DataFrame with 'TransactionDateTime' and 'TransactionValue' columns.
    """
    data = df.copy()
    st.header("Revenue Breakdown")

    # Calculate the cutoff date for the last two years
    cutoff_date = pd.to_datetime('today') - pd.DateOffset(years=2)
    chart_data = data[data['TransactionDateTime'] >= cutoff_date].sort_values('TransactionDateTime')

    col1, col2 = st.columns(2)

    # --- Daily Revenue Chart ---
    st.header("Total Daily Revenue (Last 2 Years)")
    daily_revenue = chart_data.set_index('TransactionDateTime').resample('D')['TransactionValue'].sum()
    col1.line_chart(daily_revenue)
    
    total_sales = data['TransactionValue'].sum()
    average_sales = data['TransactionValue'].mean()
    total_orders = len(data)

    col2.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Average Sale", f"${average_sales:,.2f}")
    col2.metric("Total Orders", f"{total_orders:,}")