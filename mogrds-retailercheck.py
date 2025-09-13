import streamlit as st
import pandas as pd

# Predefined known retailer domains
KNOWN_RETAILERS = {
    "dollartree.com": "Dollar Tree",
    "circlek.com": "Circle K",
    "shell.com": "Shell",
    "walmart.com": "Walmart",
    "target.com": "Target",
    "dollargeneral.com": "Dollar General",
    "7-eleven.com": "7-Eleven",
    "costco.com": "Costco",
    "amazon.com": "Amazon",
    "kroger.com": "Kroger",
    "walgreens.com": "Walgreens",
    "cvs.com": "CVS",
    "aldi.us": "Aldi",
    "riteaid.com": "Rite Aid",
    "publix.com": "Publix",
    "bestbuy.com": "Best Buy",
    "lowes.com": "Lowe's",
    "homedepot.com": "Home Depot"
}

def clean_description(desc):
    return desc.lower().replace(" ", "").replace("-", "").replace(".", "")

def match_retailer(cleaned_desc):
    matched = [domain for domain in KNOWN_RETAILERS if cleaned_desc in domain.replace(".", "").lower()]
    if len(matched) == 1:
        return matched[0], "Yes"
    else:
        return "", "No"

st.title("Retailer Identification from Description")

uploaded_file = st.file_uploader("Upload a CSV or Excel file with a 'Description' column", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        st.error("Unsupported file format.")
        st.stop()

    if "Description" not in df.columns:
        st.error("The file must contain a 'Description' column.")
    else:
        retailer_names = []
        statuses = []

        for desc in df["Description"]:
            cleaned = clean_description(str(desc))
            retailer, status = match_retailer(cleaned)
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
