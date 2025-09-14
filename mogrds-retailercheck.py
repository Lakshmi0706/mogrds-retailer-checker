import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse
from io import BytesIO

st.title("Retailer Search Validator")

# Upload file
uploaded_file = st.file_uploader("Upload a file containing descriptions", type=["csv", "xlsx"])

# Input SerpAPI key
api_key = st.text_input("Enter your SerpAPI key")

# List of known non-retail domains to ignore
non_retail_domains = {
    "instagram.com", "facebook.com", "linkedin.com", "youtube.com", "twitter.com",
    "pinterest.com", "tiktok.com", "reddit.com", "wikipedia.org", "yelp.com"
}

def extract_retailer_name(result):
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    for text in [title, snippet]:
        words = text.split()
        for word in words:
            word_clean = word.strip(",.()").lower()
            if word_clean not in non_retail_domains and word_clean.isalpha():
                return word_clean.title()
    return None

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

            retailers = set()
            if "organic_results" in data:
                for result in data["organic_results"]:
                    link = result.get("link", "")
                    domain = urlparse(link).netloc.replace("www.", "")
                    if domain not in non_retail_domains:
                        retailer_name = extract_retailer_name(result)
                        if retailer_name:
                            retailers.add(retailer_name)

            if len(retailers) == 1:
                df.at[i, 'retailer'] = list(retailers)[0]
                df.at[i, 'status'] = 'Yes'
            else:
                df.at[i, 'retailer'] = ', '.join(retailers)
                df.at[i, 'status'] = 'No'

        st.write("Updated Data:")
        st.dataframe(df)

        output = BytesIO()
        df.to_csv(output, index=False)
        st.download_button("Download Updated CSV", output.getvalue(), file_name="updated_data.csv", mime="text/csv")
