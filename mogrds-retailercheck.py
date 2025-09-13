import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote

# Replace with your actual SerpAPI key
SERPAPI_API_KEY = "your_serpapi_key_here"

def search_with_serpapi(description):
    query = f"{description} USA"
    url = f"https://serpapi.com/search.json?q={quote(query)}&location=United States&hl=en&gl=us&api_key={SERPAPI_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if "organic_results" not in data:
            return "", "No"

        domains = set()
        for result in data["organic_results"]:
            link = result.get("link", "")
            if link:
                domain = link.split("/")[2] if "://" in link else link.split("/")[0]
                domains.add(domain)

        # Clean description for matching
        desc_clean = description.lower().replace(" ", "").replace("-", "")
        matched = [d for d in domains if desc_clean in d.replace(".", "").lower()]

        if len(matched) == 1 and len(domains) == 1:
            return matched[0], "Yes"
        else:
            return "", "No"
    except Exception:
        return "", "No"

st.title("Retailer Identification via SerpAPI (Exact Match Logic)")
uploaded_file = st.file_uploader("Upload a CSV or Excel file with a 'Description' column", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    if "Description" not in df.columns:
        st.error("The file must contain a 'Description' column.")
    else:
        st.write("Processing descriptions using SerpAPI...")
        retailer_names = []
        statuses = []

        for desc in df["Description"]:
            retailer, status = search_with_serpapi(desc)
            retailer_names.append(retailer)
            statuses.append(status)

        df["Retailer Name"] = retailer_names
        df["Status"] = statuses

        st.success("Processing complete!")
        st.dataframe(df)

        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df(df)
        st.download_button("Download Updated File", csv, "updated_results.csv", "text/csv")
