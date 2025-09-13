import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of descriptions
descriptions = [
    "SHELL FILL UP",
    "E&H ACE RICHMOND HTS E&H ACE HARDWARE",
    "THE HOME DRPCC",
    "98 GAS N GO BUENA"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_domains_from_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    domains = set()
    for link in links:
        href = link.get("href")
        if href and "/url?q=" in href:
            try:
                domain = href.split("/url?q=")[1].split("&")[0].split("/")[2]
                domains.add(domain)
            except IndexError:
                continue
    return domains

results = []

for desc in descriptions:
    query = f"{desc} USA"
    print(f"Searching for: {query}")
    domains = get_domains_from_google(query)
    time.sleep(2)  # polite delay to avoid being blocked

    if len(domains) == 1:
        retailer_name = list(domains)[0]
        status = "Yes"
    else:
        retailer_name = ", ".join(domains)
        status = "No"

    results.append({
        "Description": desc,
        "Retailer Name": retailer_name,
        "Status": status
    })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("retailer_results.csv", index=False)
print("Results saved to retailer_results.csv")
