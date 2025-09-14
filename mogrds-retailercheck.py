st.title("Retailer Domain Validator")

api_key = st.text_input("Enter your SerpAPI API Key", type="password")
uploaded_file = st.file_uploader("Upload CSV file with 'description' column", type=["csv"])

if uploaded_file and api_key:
    df = pd.read_csv(uploaded_file)
    results = []
    for desc in df["description"]:
        domains, retailer = query_serpapi(desc, api_key)
        status = "Yes" if len(domains) == 1 else "No"
        results.append({"description": desc, "retailer": retailer, "status": status})
    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Results CSV", csv, "retailer_results.csv", "text/csv")
