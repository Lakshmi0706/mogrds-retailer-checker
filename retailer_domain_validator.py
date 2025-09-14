def extract_unique_domain(search_results):
    domains = set()
    retailer_name = None
    for result in search_results.get("organic_results", []):
        if "link" in result:
            domain = result["link"].split("/")[2]  # Extract domain
            domains.add(domain)
            if not retailer_name and "title" in result:
                retailer_name = result["title"]
    return domains, retailer_name
