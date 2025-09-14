import streamlit as st
import pandas as pd
import requests
import re

# Function to clean retailer title
def clean_title(title):
    return re.split(r"[|\\-]", title)[0].strip()

# Function to extract domain from URL
def extract_domain(url):
    try:
        return url.split("/")[2]
    except IndexError:
        return ""

# Function to query SerpAPI and process results
def query_serpapi(description, api_key):
    search_query = f"{description} USA"
    params = {
        "engine": "google",
        "q": search_query,
        "api_key": api_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    domains = set()
    retailer_name = None

    for result in data.get("organic_results", []):
        link = result.get("link", "")
        title = result.get("title", "")
        domain = extract_domain(link)
        if domain:
            domains.add(domain)
        if not retailer_name and title:
            retailer_name = clean_title(title)

    return domains, retailer_name or ""

# Streamlit UI
st.title("Retailer Domain Validator")

api_key = st.text_input("Enter your SerpAPI API Key", type="password")
uploaded_file = st.file_uploader("Upload CSV file with 'description' column", type=["csv"])

if uploaded_file and api_key:
    df = pd.read_csv(uploaded_file)
    if "description" not in df.columns:
        st.error("CSV must contain a 'description' column.")
    else:
        results = []
        for desc in df["description"]:
            domains, retailer = query_serpapi(desc, api_key)
            status = "Yes" if len(domains) == 1 else "No"
            results.append({"description": desc, "retailer": retailer, "status": status})
        result_df = pd.DataFrame(results)
        st.success("Processing complete.")
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results CSV", csv, "retailer_results.csv", "text/csv")

