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
    
    # Revenue breakdown by location
    st.header("Total Revenue")
    revenue_by_location = data.groupby('Location')['TransactionValue'].sum()
    pie_data = [{"value": round(value), "name": name} for name, value in revenue_by_location.items()]

    col1, col2 = st.columns(2, gap="large", border= True)
    with col1:
        topRevenueContainer = st.container()
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

    # Specific Location Information
    REGION_LOCATIONS = {
        "Auckland": ["Albany", "Auckland Central", "Botany", "Domain", "Glen Eden", "Glen Innes", "Henderson", "Lincoln Road", "Manukau", "Manukau Centre", "MT Wellington", "New Lynn", "Pakuranga", "Pukekohe", "Queen Street", "Rosebank Road", "Sylvia Park", "Takanini", "Westgate", "Warkworth", "Williams Drive"],
        "Bay of Plenty": ["Bethlehem", "Gate Pa", "Rotorua", "Whakatane"],
        "Canterbury": ["Ashburton", "Christchurch (Papanui, Riccarton)", "Ferryhead", "Hornby", "Rangiora", "Timaru"],
        "Gisborne": ["Gisborne"],
        "Hawke's Bay": ["Hastings", "Napier"],
        "Manawatū-Whanganui": ["Levin", "Palmerston Nth", "Wanganui"],
        "Marlborough": ["Marlborough"],
        "Nelson": ["Nelson"],
        "Otago": ["Dunedin", "Oamaru", "Queenstown"],
        "Southland": ["Invercargill"],
        "Taranaki": ["New Plymouth"],
        "Tasman": ["Richmond"],
        "Waikato": ["Cambridge", "Ruakura", "Te Awamutu", "Te Rapa", "Taupo"],
        "Wellington": ["Aubyn", "Broadway", "Crofton Downs", "Kapiti", "London St", "Masterton", "Newtown", "Petone", "Porirua", "Upper Hutt", "Wellington central"],
        "West Coast": ["Greymouth"]
    }
    regions = ["All"] + list(REGION_LOCATIONS.keys())
    
    col1, col2, col3, col4 = st.columns([1.2, 0.5, 0.5, 3])
    with col1:
        st.header("Revenue Breakdown")
    
    with col2:
        region = st.selectbox(
            "Region",
            regions,
            index=0,
        )

    locations_in_region = ["All"]
    if region != "All":
        locations_in_region.extend(REGION_LOCATIONS[region])
    else:
        # If 'All' regions, show all unique locations from the dataframe
        locations_in_region.extend(sorted(data['Location'].unique().tolist()))

    with col3:
        location = st.selectbox(
            "Location",
            locations_in_region,
            index=0,
        )

    filtered_data = data.copy()
    if region != "All":
        filtered_data = filtered_data[filtered_data['Location'].isin(REGION_LOCATIONS[region])]
    
    if location != "All":
        filtered_data = filtered_data[filtered_data['Location'] == location]
    
    # Calculate the cutoff date for the last two years
    cutoff_date = pd.to_datetime('today') - pd.DateOffset(years=2)
    chart_data = filtered_data[filtered_data['TransactionDateTime'] >= cutoff_date].sort_values('TransactionDateTime')

    

    col1, col2 = st.columns(2, gap='large')

    # Daily Revenue Chart
    daily_revenue = chart_data.set_index('TransactionDateTime').resample('D')['TransactionValue'].sum()
    chart_container = col1.container(border=True, height=400)
    chart_container.line_chart(daily_revenue, color="#5D4037")
    
    total_sales = filtered_data['TransactionValue'].sum()
    average_sales = filtered_data['TransactionValue'].mean()
    total_orders = len(filtered_data)

    with col2:
        revenueMetricContainer = st.container(border=True, height=400)
        revenueMetricContainer.metric("Total Sales", f"${total_sales:,.2f}")
        revenueMetricContainer.metric("Average Sale", f"${average_sales:,.2f}")
        revenueMetricContainer.metric("Total Orders", f"{total_orders:,}")






