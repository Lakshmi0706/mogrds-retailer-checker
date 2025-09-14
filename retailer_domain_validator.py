import streamlit as st
import pandas as pd

# Sample mapping of known retailers (expand as needed)
retailer_mapping = {
    "DULLAR REE": "Dollar Tree",
    "OUILET GROCERY": "Grocery Outlet",
    "PRICE HOUPER": "Price Chopper",
    "1 CIRCLE K": "Circle K",
    "RACEXRAC": "RaceTrac",
    "SHELL AUGUSTINE SHEL SHELL": "Shell",
    "REMARKABLY FRESH. CASH WISE FRIENDLY INCREDIBLY LIOUOR": "Cash Wise",
    "THIE HOM DPPOT": "The Home Depot",
    "SEYMOUR FOODMART SEYMOUR XTRA MART": "Xtra Mart",
    "FOOD EZ MART LIQUOR": "EZ Mart",
    "LF MARATHON LF MARATHON": "Marathon Petroleum",
    "SHOFPING WEIS MARKETS": "Weis Markets",
    "FOE DD BAZAAR SUPERMARKET": "Food Bazaar Supermarket",
    "THE HOT DBPOT": "The Home Depot",
    "SPR DUTS FARM ERS MARKET": "Sprouts Farmers Market",
    "TIBLE HERBST": "Terrible's (Terrible Herbst)"
}

st.title("Retailer Validation App")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean and process
    df["Retailer"] = ""
    df["Result"] = "No"

    for i, row in df.iterrows():
        desc = str(row["description"]).strip().upper()
        retailer = retailer_mapping.get(desc)
        if retailer:
            df.at[i, "Retailer"] = retailer
            df.at[i, "Result"] = "Yes"

    st.success("Validation complete!")
    st.dataframe(df)

    # Download link
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Updated CSV", csv, "validated_retailers.csv", "text/csv")
