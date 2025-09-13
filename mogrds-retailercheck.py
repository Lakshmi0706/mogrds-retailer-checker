import streamlit as st
import pandas as pd
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")
    except:
        return ""

st.title("Manual Retailer Identification via Google Search")

uploaded_file = st.file_uploader("Upload a CSV or Excel file with a 'Description' column", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    if "Description" not in df.columns:
        st.error("The file must contain a 'Description' column.")
    else:
        st.write("Step 1: Manually search each description on Google and paste the top result URL below.")

        urls = []
        for i, desc in enumerate(df["Description"]):
            url = st.text_input(f"Top Google result for '{desc}'", key=f"url_{i}")
            urls.append(url)

        retailer_names = []
        statuses = []

        for url in urls:
            domain = extract_domain(url)
            if domain:
                retailer_names.append(domain)
                statuses.append("Yes")
            else:
                retailer_names.append("")
                statuses.append("No")

        df["Retailer Name"] = retailer_names
        df["Status"] = statuses

        st.success("Processing complete!")
        st.dataframe(df)

        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df(df)
        st.download_button("Download Updated File", csv, "updated_results.csv", "text/csv")
