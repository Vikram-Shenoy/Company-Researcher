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
        raise Exception(f"--------------------No 10-K filings found for this company. Possibly an unlisted or foreign company-----------------------\n")
    
    latest_filing = filings["filings"][0]  # Get the most recent filing
    # documents = latest_filing.get("documentFormatFiles", [])
    filing_url = latest_filing["linkToFilingDetails"]

    # for doc in documents:
    #     description = doc.get("description", "").lower()  # Get description if available
        
    #     # Check if the description contains '10-k'
    #     if "10-k" in description:
    #         filing_url = doc["documentUrl"]
    #         break  # Stop once we find the correct document

    # If no '10-K' document was found, handle the error or fallback
    if not filing_url:
        raise Exception(f"No primary 10-K document found for {ticker}")
        
    print(f"\n ***Latest 10-K filings for {ticker}: {filings}***\n")
    
    # Write the filing URL to a file
    with open(f"./URLS/{ticker}_10k_url.txt", "w", encoding="utf-8") as file:
        file.write(f"Latest 10-K URL for {ticker}: {filing_url}\n")
    
    return filing_url

def extract_business_section(filing_url, ticker):
    """Extract the 'Item 1. Business' section from a given 10-K filing URL"""
    
    business_section = extractorApi.get_section(filing_url, "1", "text")
    
    print(f"\n ***Extracted Business Section for {ticker}:***\n")
    print(business_section[:1000] + "...\n")  # Print only first 1000 chars for preview
    
    # Write the extracted text to a file
    with open(f"./Business Section/{ticker}_business_section.txt", "w", encoding="utf-8") as file:
        file.write(business_section)
    
    return business_section

def main():
    ticker = input("Enter the ticker symbol: ").strip().upper()  # Example: AAPL, KO, TSLA
    print(ticker)
    filing_url = get_latest_10k_url(ticker)
    extract_business_section(filing_url, ticker)
    print(f"\n✅ Business section saved to {ticker}_business_section.txt")

if __name__ == "__main__":
    main()
