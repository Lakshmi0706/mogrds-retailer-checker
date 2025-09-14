# Corrected Streamlit app code creation and push to GitHub repo folder

import os

# Define the corrected Streamlit app code
corrected_code = '''
import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse
from io import BytesIO

st.title("Retailer Domain Validator")

uploaded_file = st.file_uploader("Upload a file containing descriptions", type=["csv", "xlsx"])
api_key = st.text_input("Enter your SerpAPI key")

# List of known non-retail domains to ignore
non_retail_domains = {
    "instagram.com", "facebook.com", "linkedin.com", "youtube.com", "twitter.com",
    "pinterest.com", "tiktok.com", "reddit.com", "wikipedia.org", "yelp.com", "google.com"
}

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
                    link = result.get("link", "")
                    domain = urlparse(link).netloc.replace("www.", "")
                    if domain and domain not in non_retail_domains:
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
'''

# Create the destination repo folder
repo_folder = "mogrds-retailer-checker"
os.makedirs(repo_folder, exist_ok=True)

# Save the corrected app code to retailer_domain_validator.py
app_file_path = os.path.join(repo_folder, "retailer_domain_validator.py")
with open(app_file_path, "w") as f:
    f.write(corrected_code)

# Update README to reflect the main file
readme_path = os.path.join(repo_folder, "README.md")
with open(readme_path, "w") as readme:
    readme.write("# Retailer Domain Validator\n\n")
    readme.write("This Streamlit app uses `retailer_domain_validator.py` as the main file.\n")
    readme.write("To deploy on Streamlit Cloud, set `retailer_domain_validator.py` as the main file.\n")

print("Corrected app file and README have been saved to the GitHub repo folder.")

