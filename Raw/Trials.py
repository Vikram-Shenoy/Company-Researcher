from sec_api import QueryApi, ExtractorApi
import os
from dotenv import load_dotenv
load_dotenv()


SEC_API_KEY = os.getenv("sec_api_key")


# Initialize APIs
queryApi = QueryApi(api_key=SEC_API_KEY)
extractorApi = ExtractorApi(api_key=SEC_API_KEY)

def get_latest_10k_url(ticker):
    """Fetch the latest 10-K filing URL for a given ticker symbol"""
    
    query = {
        "query": f"ticker:{ticker} AND filedAt:[2024-01-01 TO 2025-12-31] AND formType:\"10-K\"",
        "from": "0",
        "size": "1",  # Get only the latest filing
        "sort": [{ "filedAt": { "order": "desc" } }]
    }
    print("Inside get_latest_10k_url, here is the query:",query)
    filings = queryApi.get_filings(query)
    
    if not filings.get("filings"):
        raise Exception(f"No 10-K filings found for {ticker}")
    
    latest_filing = filings["filings"][0]  # Get the most recent filing
    documents = latest_filing.get("documentFormatFiles", [])
    filing_url = None

    for doc in documents:
        description = doc.get("description", "").lower()  # Get description if available
        
        # Check if the description contains '10-k'
        if "10-k" in description:
            filing_url = doc["documentUrl"]
            break  # Stop once we find the correct document

    # If no '10-K' document was found, handle the error or fallback
    if not filing_url:
        raise Exception(f"No primary 10-K document found for {ticker}")
        
    print(f"\n✅ Latest 10-K filings for {ticker}: {filings}\n")
    
    # Write the filing URL to a file
    with open(f"{ticker}_10k_url.txt", "w", encoding="utf-8") as file:
        file.write(f"Latest 10-K URL for {ticker}: {filings}\n")
    
    return filing_url


ticker = input("Enter the ticker symbol: ").strip().upper()  # Example: AAPL, KO, TSLA
print(ticker)
filing_url = get_latest_10k_url(ticker)

print("Here's your filing URL:", filing_url)