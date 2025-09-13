import streamlit as st
import pandas as pd
from googlesearch import search
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except:
        return ""

def is_unique_retailer(description, domains):
    desc_clean = description.lower().replace(" ", "").replace("-", "")
    matched_domains = [d for d in domains if desc_clean in d.replace(".", "").lower()]
    
    # If only one domain matches the cleaned description exactly
    if len(matched_domains) == 1 and len(domains) == 1:
        return matched_domains[0], "Yes"
    else:
        return "", "No"

def process_description(description):
    query = f"{description} USA"
    try:
        results = list(search(query, num_results=10))
        domains = set(extract_domain(url) for url in results if extract_domain(url))
        return is_unique_retailer(description, domains)
    except Exception:
        return "", "No"

st.title("Retailer Identification via Google Search (Exact Match Logic)")
uploaded_file = st.file_uploader("Upload a CSV or Excel file with a 'Description' column", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    if "Description" not in df.columns:
        st.error("The file must contain a 'Description' column.")
    else:
        st.write("Processing descriptions...")
        retailer_names = []
        statuses = []

        for desc in df["Description"]:
            retailer, status = process_description(desc)
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
