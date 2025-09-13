import streamlit as st
import pandas as pd
from urllib.parse import urlparse
import requests

# Function to perform Google search using SerpAPI
def search_google(description, api_key):
    query = f"{description} USA"
    params = {
        "q": query,
        "location": "United States",
        "api_key": api_key,
        "engine": "google"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    links = [result['link'] for result in data.get("organic_results", [])]
    return links

# Function to extract unique retailer domains
def get_unique_domain(links):
    domains = set(urlparse(link).netloc for link in links)
    retailer_domains = [d for d in domains if "amazon" not in d and "wikipedia" not in d and d]
    return retailer_domains

# Streamlit UI
st.title("Retailer Uniqueness Checker")

api_key = st.text_input("Enter your SerpAPI Key")

uploaded_file = st.file_uploader("Upload your description file (CSV with 'description' column)", type=["csv"])

if uploaded_file and api_key:
    df = pd.read_csv(uploaded_file)
    if 'description' not in df.columns:
        st.error("CSV must contain a 'description' column.")
    else:
        results = []
        for desc in df['description']:
            links = search_google(desc, api_key)
            unique_domains = get_unique_domain(links)
            if len(unique_domains) == 1:
                results.append({"retailer": unique_domains[0], "status": "Yes"})
            else:
                results.append({"retailer": "", "status": "No"})
        
        df_result = df.copy()
        df_result["retailer"] = [r["retailer"] for r in results]
        df_result["status"] = [r["status"] for r in results]

        st.dataframe(df_result)

        csv = df_result.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", csv, "retailer_results.csv", "text/csv")
else:
    st.info("Please upload a file and enter your SerpAPI key to proceed.")
