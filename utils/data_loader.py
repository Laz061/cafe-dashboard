import pandas as pd

def load_cafe_data(filepath):
    """
    Load the CafeData CSV, clean irregular rows, and return a consistent DataFrame.
    """

    df_raw = pd.read_csv(filepath, header=None, engine="python")
    
    cleaned_rows = []

    # Process each row, skipping the header
    for _, row in df_raw.iloc[1:].iterrows():
        # Drop empty cells (from trailing commas)
        values = row.dropna().tolist()
        
        if len(values) == 6:
            cleaned = values
        elif len(values) == 5:
            cleaned = [
                values[0],  # Location
                values[1],  # Rating
                "",  # Comment
                values[2],  # TransactionDateTime
                values[3],  # TransactionValue
                values[4]   # FeedbackID
            ]
        elif len(values) == 7:
            print(f"processing 7row: {values[0]}")
            if pd.to_datetime(values[3], errors='coerce') is pd.NaT:
                values[3] = None # Replace invalid date with None

            # Handle potential outlier value in the value field (values[4])
            try:
                transaction_value_str = str(values[4]).replace('$', '').replace(',', '')
                transaction_value = float(transaction_value_str)
                if transaction_value > 1000:
                    values[4] = '0'
            except (ValueError, IndexError):
                # If conversion fails or index is wrong, treat as outlier
                values[4] = '0'
            cleaned = [
                values[0],  # Location
                values[1],  # Rating
                values[2],  # Comment
                values[3],  # TransactionDateTime
                values[4],  # TransactionValue
                values[6]   # FeedbackID
            ]
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
            
    # Build final dataframe
    cleaned_df = pd.DataFrame(cleaned_rows, columns=[
        "Location",
        "Rating",
        "Comment",
        "TransactionDateTime",
        "TransactionValue",
        "FeedbackID"
    ])

    # Convert data types
    cleaned_df['TransactionDateTime'] = pd.to_datetime(cleaned_df['TransactionDateTime'], dayfirst=True, errors='coerce')
    cleaned_df['TransactionValue'] = pd.to_numeric(cleaned_df['TransactionValue'].astype(str).str.replace('$', '', regex=False), errors='coerce')
    cleaned_df['Rating'] = pd.to_numeric(cleaned_df['Rating'], errors='coerce')
    cleaned_df['FeedbackID'] = pd.to_numeric(cleaned_df['FeedbackID'], errors='coerce')
    cleaned_df['Location'] = cleaned_df['Location'].str.strip()

    return cleaned_df