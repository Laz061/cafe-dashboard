import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

def display_revenue_section(df):
    """
    Calculates and displays a line chart of total daily revenue for the last years.

    Args:
        df (pd.DataFrame): The input DataFrame with 'TransactionDateTime' and 'TransactionValue' columns.
    """
    # Specific Location Information
    REGION_LOCATIONS = {
        "Auckland": ["Albany", "Auckland Central", "Botany", "Domain", "Glen Eden", "Glen Innes", "Henderson", "Lincoln Road", "Manukau", "Manukau Centre", "MT Wellington", "New Lynn", "Pakuranga", "Pukekohe", "Queen Street", "Rosebank Road", "Sylvia Park", "Takanini", "Westgate", "Warkworth", "Williams Drive"],
        "Bay of Plenty": ["Bethlehem", "Gate Pa", "Rotorua", "Whakatane"],
        "Canterbury": ["Ashburton", "Ferryhead", "Hornby", "Rangiora", "Timaru"],
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

    # Use markdown with more specific CSS to create larger metric text
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > [data-testid="stMarkdownContainer"] > p {
            padding: 0.5rem 0;
        }
        .metric-value {
            font-size: 2.5rem !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
        }
        .metric-label {
            font-size: 1.5rem !important;
            color: #808495 !important; /* Streamlit's default secondary text color */
        }
        /* Smaller styles for the top locations section */
        .top-metric-value {
            font-size: 2.5rem !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
        }
        .top-metric-label {
            font-size: 1.5rem !important;
            color: #808495 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

    data = df.copy()
    # Create a reverse mapping from location to region
    location_to_region = {location: region for region, locations in REGION_LOCATIONS.items() for location in locations}
    data['Region'] = data['Location'].map(location_to_region)
    
    regions = ["All"] + list(REGION_LOCATIONS.keys())
    
    col1, col2, col3 = st.columns(3)
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
    
    # Calculate the cutoff date for the last two years to accomodate the dataset
    cutoff_date = pd.to_datetime('today') - pd.DateOffset(years=2)
    chart_data = filtered_data[filtered_data['TransactionDateTime'] >= cutoff_date].sort_values('TransactionDateTime')

    col1, col2 = st.columns(2)

    with col1:
            st.subheader("Daily Revenue")
            # Daily Revenue Chart
            daily_revenue = chart_data.set_index('TransactionDateTime').resample('D')['TransactionValue'].sum().reset_index()
            daily_revenue.rename(columns={'TransactionDateTime': 'Date', 'TransactionValue': 'Revenue'}, inplace=True)
            
            # ECharts options for a non-interactive line chart
            line_chart_options = {
                "xAxis": {
                    "type": "category",
                    "data": daily_revenue['Date'].dt.strftime('%Y-%m-%d').tolist(),
                    "name": "Date",
                    "nameLocation": "middle",
                    "nameGap": 30
                },
                "yAxis": {
                    "type": "value",
                    "name": "Revenue ($)",
                    "nameLocation": "middle",
                    "nameGap": 45
                },
                "tooltip": {
                    "trigger": "axis",
                    "formatter": "Date: {b}<br/>Revenue: ${c}",
                },
                "series": [{
                    "data": daily_revenue['Revenue'].tolist(),
                    "type": "line",
                    "smooth": True,
                    "color": "#5D4037",
                }],
            }
            st_echarts(options=line_chart_options)
    
    total_sales = chart_data['TransactionValue'].sum()
    average_sales = chart_data['TransactionValue'].mean()
    total_orders = len(chart_data)

    with col2:
        st.markdown(f"""
            <p class="metric-label">Total Revenue</p>
            <p class="metric-value">${total_sales:,.2f}</p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <p class="metric-label">Average Transaction</p>
            <p class="metric-value">${average_sales:,.2f}</p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <p class="metric-label">Total Transactions</p>
            <p class="metric-value">{total_orders:,}</p>
        """, unsafe_allow_html=True)

    # Revenue breakdown by location
    col1, col2 = st.columns(2, gap="large", border= True)
    with col1:
        topRevenueContainer = st.container()
        revenue_by_location = data.groupby('Location')['TransactionValue'].sum()
        top_locations = revenue_by_location.sort_values(ascending=False).head(6)
        topRevenueContainer.subheader("Top Locations by Revenue")
        
        cols = topRevenueContainer.columns(2)
        i = 0
        for location, revenue in top_locations.items():
            col_index = i % 2
            cols[col_index].markdown(f"""
                <p class="top-metric-label">#{i+1} {location}</p>
                <p class="top-metric-value">${revenue:,.2f}</p>
            """, unsafe_allow_html=True)
            i += 1
    with col2:
        group_by = st.radio(
            "Group Revenue By:",
            ('Region', 'Location'),
            horizontal=True,
        )

        if group_by == 'Location':
            revenue_grouped = data.groupby('Location')['TransactionValue'].sum()
        else: # group_by == 'Region'
            revenue_grouped = data.groupby('Region')['TransactionValue'].sum()

        pie_data = [{"value": round(value), "name": name} for name, value in revenue_grouped.items()]

        # Pie chart setup
        options = {
        "tooltip": {"trigger": "item"},
        "series": [
            {
                "name": "Revenue",
                "type": "pie",
                "radius": ["40%", "80%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False},
                "emphasis": {
                },
                "labelLine": {"show": False},
                "data": pie_data,
            }
        ],}
        st_echarts(options=options, height="450px")








