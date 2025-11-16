import streamlit as st
import pandas as pd
from openai import OpenAI
from streamlit_echarts import st_echarts
from pathlib import Path

def display_ai_section(df):
    st.header("AI Analysis")

    analysis_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if st.button("Analyse Data"):
        try:
            prompt_path = Path(__file__).parent / "analysis_prompt.txt"
            with open(prompt_path, "r") as f:
                system_prompt = f.read()

            data_csv = df.to_csv(index=False)
            user_prompt = f"hello"

            with st.spinner("AI is analyzing the data..."):
                response = analysis_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                analysis_result = response.choices[0].message.content
                st.markdown(analysis_result)
        except FileNotFoundError:
            st.error("The 'analysis_prompt.txt' file was not found. Please create it in the 'utils' directory.")
        except Exception as e:
            st.error(f"An error occurred during AI analysis: {e}")