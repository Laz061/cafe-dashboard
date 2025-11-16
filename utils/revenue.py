import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

def display_revenue_section(df):
    """
    Calculates and displays a line chart of total daily revenue for the last years.

    Args:
        df (pd.DataFrame): The input DataFrame with 'TransactionDateTime' and 'TransactionValue' columns.
    """
    data = df.copy()
    data['Location'] = data['Location'].str.strip()

    # Calculate the cutoff date for the last two years
    cutoff_date = pd.to_datetime('today') - pd.DateOffset(years=2)
    chart_data = data[data['TransactionDateTime'] >= cutoff_date].sort_values('TransactionDateTime')

    st.header("Revenue Breakdown")

    col1, col2 = st.columns(2, gap='large')

    # Daily Revenue Chart
    daily_revenue = chart_data.set_index('TransactionDateTime').resample('D')['TransactionValue'].sum()
    chart_container = col1.container(border=True, height=400)
    chart_container.line_chart(daily_revenue, use_container_width=True)
    
    total_sales = data['TransactionValue'].sum()
    average_sales = data['TransactionValue'].mean()
    total_orders = len(data)

    with col2:
        revenueMetricContainer = st.container(border=True, height=400)
        revenueMetricContainer.metric("Total Sales", f"${total_sales:,.2f}")
        revenueMetricContainer.metric("Average Sale", f"${average_sales:,.2f}")
        revenueMetricContainer.metric("Total Orders", f"{total_orders:,}")
    
    # Revenue breakdown by location
    st.header("Revenue by Location")
    revenue_by_location = data.groupby('Location')['TransactionValue'].sum()
    pie_data = [{"value": round(value), "name": name} for name, value in revenue_by_location.items()]

    col1, col2 = st.columns(2, gap="large")
    with col1:
        topRevenueContainer = st.container(border=True, height=500)
        top_locations = revenue_by_location.sort_values(ascending=False).head(6)
        topRevenueContainer.subheader("Top Locations by Revenue")
        
        cols = topRevenueContainer.columns(2)
        i = 0
        for location, revenue in top_locations.items():
            col_index = i % 2
            cols[col_index].metric(label=f"#{i+1} {location}", value=f"${revenue:,.2f}")
            i += 1
    with col2:
        # Pie chart setup
        options = {
        "tooltip": {"trigger": "item"},
        "series": [
            {
                "name": "Revenue By Location",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                },
                "labelLine": {"show": False},
                "data": pie_data,
            }
        ],}
        st_echarts(options=options, height="500px")
    



