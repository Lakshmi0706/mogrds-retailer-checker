import streamlit as st
from googlesearch import search

def check_unique_retailer(description):
    query = f"{description} USA"
    try:
        links = list(search(query, num_results=10))
        retailer_domains = [link.split('/')[2] for link in links if 'http' in link and 'google' not in link]
        unique_domains = set(retailer_domains)

        if len(unique_domains) == 1:
            return "yesclean", list(unique_domains)[0]
        else:
            return "not clear", list(unique_domains)
    except Exception as e:
        return "error", str(e)

st.title("Retailer Uniqueness Checker")

descriptions = st.text_area("Enter descriptions (one per line):")
if st.button("Check Retailers"):
    if descriptions:
        desc_list = descriptions.strip().split('\n')
        for desc in desc_list:
            status, site = check_unique_retailer(desc)
            st.write(f"{desc}: {status}")
            st.write(f"Retailer: {site}")
