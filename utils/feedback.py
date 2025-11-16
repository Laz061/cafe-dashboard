import streamlit as st
import pandas as pd

# --- Function to Draw Star Icons ---
def draw_stars(rating, max_stars=5):
    """Generates HTML string for filled and empty star icons."""
    filled_stars = '★' * int(rating)
    empty_stars = '☆' * (max_stars - int(rating))
    return f'<span style="color:#c9935c;">{filled_stars}</span>{empty_stars}'

def display_feedback_section(df):
    st.markdown(
        """
        <style>
        .big-font {
            font-size: 5rem !important;
            font-weight: 700;
            line-height: 1.0;
            margin: 0;
        }
        .rating-label {
            color: #7d7d7d;
            font-weight: 500;
        }
        .stProgress > div > div > div > div {
            background-color: #c9935c; /* Custom color for the progress bar */
            height: 8px; /* Making the bar thinner */
            border-radius: 4px;
        }
        .stProgress > div > div {
            background-color: #f0f0f0; /* Background color of the track */
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    data = df.copy()

    # Define regions and their locations
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
        st.header("Customer Ratings")
    with col2:
        region = st.selectbox(
            "Region",
            regions,
            index=0,
            key="feedback_region"
        )

    locations_in_region = ["All"]
    if region != "All":
        locations_in_region.extend(REGION_LOCATIONS[region])
    else:
        # If 'All' regions, show all unique locations from the dataframe
        locations_in_region.extend(sorted(df['Location'].unique().tolist()))

    with col3:
        location = st.selectbox(
            "Location",
            locations_in_region,
            index=0,
            key="feedback_location"
        )
        
    # Filter data based on selection
    if region != "All":
        data = data[data['Location'].isin(REGION_LOCATIONS[region])]
    
    if location != "All":
        data = data[data['Location'] == location]

    #Data processing
    total_reviews = len(data["Rating"])
    average_rating = data['Rating'].mean() if not data.empty else 0
    rating_counts = data['Rating'].value_counts().sort_index(ascending=False)

    # Create two columns for the rating breakdown
    col_left, col_right = st.columns([1, 2.5])

    # --- Left Column: Overall Average Rating ---
    with col_left:
        # Format the average rating to one decimal place
        avg_rating_str = f"{average_rating:.1f}"
        
        # Display the large average rating
        st.markdown(f'<p class="big-font">{avg_rating_str}</p>', unsafe_allow_html=True)
        
        # Display the star representation
        st.markdown(draw_stars(average_rating), unsafe_allow_html=True)
        
        # Display the total number of reviews
        st.markdown(f"**{total_reviews} reviews**")

    # --- Right Column: Star Breakdown Bars ---
    with col_right:
        # Iterate from 5 stars down to 1 star
        for rating in range(5, 0, -1):
            # Get the count for the current rating, default to 0 if none
            count = rating_counts.get(rating, 0)
            
            # Calculate the percentage for the bar width
            percentage = count / total_reviews if total_reviews > 0 else 0
            
            # Create a row of three inner columns for layout: [Star Label] [Progress Bar] [Count]
            row_col1, row_col2, row_col3 = st.columns([0.5, 3, 0.5])
            
            # Column 1: Star label (e.g., '5 ★')
            with row_col1:
                # Use markdown for consistent styling and a custom class for alignment/color
                st.markdown(
                    f'<div class="rating-label">{rating} {draw_stars(rating)}</div>',
                    unsafe_allow_html=True
                )

            # Column 2: Progress Bar
            with row_col2:
                # Use st.progress to draw the bar based on the percentage
                st.progress(percentage)

            # Column 3: Count
            with row_col3:
                st.markdown(f'<div style="text-align: right;">{count}</div>', unsafe_allow_html=True)

    # --- Feedback Section ---
    st.header("Customer Feedback")

    # Sort by rating to get top and bottom feedback
    top_feedback = data.sort_values(by='Rating', ascending=False).head(3)
    bottom_feedback = data.sort_values(by='Rating', ascending=True).head(3)

    col_pos, col_neg = st.columns(2)

    with col_pos:
        st.subheader("Top Positive Feedback")
        for _, row in top_feedback.iterrows():
            location = row['Location']
            rating = row['Rating']
            comment = row['Comment']
            date = row['TransactionDateTime'].strftime('%d/%m/%Y')
            
            st.markdown(
                f"""
                **{location}** {draw_stars(rating)}  
                *{comment}*  
                <small>{date}</small>
                <hr style="margin: 5px 0 5px 0;">
                """,
                unsafe_allow_html=True
            )

    with col_neg:
        st.subheader("Areas for Improvement")
        for _, row in bottom_feedback.iterrows():
            location = row['Location']
            rating = row['Rating']
            comment = row['Comment']
            date = row['TransactionDateTime'].strftime('%d/%m/%Y')

            st.markdown(
                f"""
                **{location}** {draw_stars(rating)}  
                *{comment}*  
                <small>{date}</small>
                <hr style="margin: 5px 0 5px 0;">
                """,
                unsafe_allow_html=True
            )