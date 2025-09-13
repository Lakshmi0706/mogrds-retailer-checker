# streamlit_app.py

import streamlit as st
import pandas as pd
from googlesearch import search
from urllib.parse import urlparse

def get_unique_domain(description):
    query = f"{description} USA"
    try:
        results = list(search(query, num_results=10))
        domains = set()
        for url in results:
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain:
                domains.add(domain)
        if len(domains) == 1:
            return list(domains)[0], "Yes"
        else:
            return "", "No"
    except Exception as e:
        return "", "No"

st.title("Retailer Identification via Google Search (No API)")
uploaded_file = st.file_uploader("Upload a CSV or Excel file with a 'Description' column", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if "Description" not in df.columns:
        st.error("The file must contain a 'Description' column.")
    else:
        st.write("Processing descriptions...")
        retailer_names = []
        statuses = []

        for desc in df["Description"]:
            retailer, status = get_unique_domain(desc)
            retailer_names.append(retailer)
            statuses.append(status)

        df["Retailer Name"] = retailer_names
        df["Status"] = statuses

        st.success("Processing complete!")
        st.dataframe(df)

        # Download button
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df(df)
        st.download_button("Download Updated File", csv, "updated_results.csv", "text/csv")
