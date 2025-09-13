import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_google(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a['href'] for a in soup.select('a') if 'url?q=' in a['href']]
    return links

def check_unique_retailer(description):
    query = f"{description} USA"
    links = search_google(query)
    retailer_domains = [link.split('/')[2] for link in links if 'http' in link and 'google' not in link]
    unique_domains = set(retailer_domains)
    if len(unique_domains) == 1:
        return "yesclear", list(unique_domains)[0]
    else:
        return "not clear", list(unique_domains)

st.title("Retailer Uniqueness Checker")

descriptions = st.text_area("Enter descriptions (one per line):")
if st.button("Check Retailers"):
    if descriptions:
        desc_list = descriptions.strip().split('\n')
        for desc in desc_list:
            status, site = check_unique_retailer(desc)
            st.write(f"*{desc}* → {status}")
            st.write(f"Retailer: {site}")
