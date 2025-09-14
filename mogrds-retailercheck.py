import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse
from io import BytesIO

st.title("Retailer Search Validator")

uploaded_file = st.file_uploader("Upload a file containing descriptions", type=["csv", "xlsx"])
api_key = st.text_input("Enter your SerpAPI key")

if uploaded_file and api_key:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    if 'description' not in df.columns:
        st.error("The uploaded file must contain a column named 'description'.")
    else:
        df['retailer'] = ''
        df['status'] = ''

        for i, desc in enumerate(df['description']):
            query = f"{desc} USA"
            params = {
                "engine": "google",
                "q": query,
                "api_key": api_key
            }
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()

            domains = set()
            if "organic_results" in data:
                for result in data["organic_results"]:
                    if "link" in result:
                        domain = urlparse(result["link"]).netloc
                        domains.add(domain)

            if len(domains) == 1:
                df.at[i, 'retailer'] = list(domains)[0]
                df.at[i, 'status'] = 'Yes'
            else:
                df.at[i, 'retailer'] = ', '.join(domains)
                df.at[i, 'status'] = 'No'

        st.write("Updated Data:")
        st.dataframe(df)

        output = BytesIO()
        df.to_csv(output, index=False)
        st.download_button("Download Updated CSV", output.getvalue(), file_name="updated_data.csv", mime="text/csv")
