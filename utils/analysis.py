import streamlit as st
import pandas as pd
from pathlib import Path
from openai import OpenAI

@st.cache_data(show_spinner="AI is analyzing the data...", ttl=86400)
def get_ai_analysis(data_csv):
    """
    Gets AI analysis from OpenAI API and caches the result globally
    for all users and sessions.
    """
    try:
        prompt_path = Path(__file__).parent / "analysis_prompt.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        st.error("The 'analysis_prompt.txt' file was not found. Please create it in the 'utils' directory.")
        return None

    user_prompt = f"Analyse the following customer data and provide insights:\n\n{data_csv}"
    
    try:
        analysis_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = analysis_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred during AI analysis: {e}")
        return None

def display_ai_section(df):

    st.header("Summary")
 
    if st.button("Generate Summary"):
        st.cache_data.clear()
        st.rerun()

    data_csv = df.to_csv(index=False)

    analysis_result = get_ai_analysis(data_csv)
    
    if analysis_result:
        st.markdown(analysis_result)