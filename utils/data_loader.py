import pandas as pd

def load_cafe_data(filepath):
    """
    Load the CafeData CSV, clean irregular rows, and return a consistent DataFrame.
    """

    df_raw = pd.read_csv(filepath, header=None, engine="python")
    
    cleaned_rows = []

    # Step 2: Process each row, skipping the header
    for _, row in df_raw.iloc[1:].iterrows():
        # Drop empty cells (from trailing commas)
        values = row.dropna().tolist()

        if len(values) >= 6:
            # Assume first 6 meaningful columns:
            if len(values) == 6:
                cleaned = values
            elif len(values) == 8:
                # Special row format: [Location, Rating, Comment, WEB, Date, Value, StoreCode, FeedbackID]
                cleaned = [
                    values[0],  # Location
                    values[1],  # Rating
                    values[2],  # Comment
                    values[4],  # TransactionDateTime
                    values[5],  # TransactionValue
                    values[7]   # FeedbackID
                ]

            cleaned_rows.append(cleaned)
        else:
            # Row too short (currently no data in this form)
            print("Skipping malformed row:", values)

    # Step 3: Build final dataframe
    cleaned_df = pd.DataFrame(cleaned_rows, columns=[
        "Location",
        "Rating",
        "Comment",
        "TransactionDateTime",
        "TransactionValue",
        "FeedbackID"
    ])

    # Convert data types
    cleaned_df['TransactionDateTime'] = pd.to_datetime(cleaned_df['TransactionDateTime'], dayfirst=True)
    cleaned_df['TransactionValue'] = pd.to_numeric(cleaned_df['TransactionValue'].str.replace('$', '', regex=False))
    cleaned_df['Rating'] = pd.to_numeric(cleaned_df['Rating'])
    cleaned_df['FeedbackID'] = pd.to_numeric(cleaned_df['FeedbackID'])

    return cleaned_df