import requests
import json
import re
from bs4 import BeautifulSoup

SEC_TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_BASE_URL = "https://www.sec.gov"

HEADERS = {
    "User-Agent": "MyCompanyName (myemail@example.com)"  # Replace with your contact info
}

def get_cik_from_ticker(ticker):
    """Convert a ticker symbol to a CIK"""
    response = requests.get(SEC_TICKER_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception("Failed to fetch CIK data")
    
    cik_mapping = response.json()
    
    for company in cik_mapping.values():
        if company["ticker"].lower() == ticker.lower():
            return str(company["cik_str"]).zfill(10)  # Ensure it's 10 digits
    
    raise Exception("Ticker not found in SEC database")

def get_latest_10k_url(cik):
    """Fetch the latest 10-K filing URL for the given CIK"""
    sec_api_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(sec_api_url, headers=HEADERS)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch company filings")
    
    filings = response.json()
    
    # Find latest 10-K
    for i, form in enumerate(filings["filings"]["recent"]["form"]):
        if form == "10-K":
            accession_number = filings["filings"]["recent"]["accessionNumber"][i]
            filing_url = f"{SEC_BASE_URL}/Archives/edgar/data/{cik}/{accession_number.replace('-', '')}/index.json"
            return filing_url
    
    raise Exception("No 10-K filing found for this company")

def get_10k_html_url(filing_index_url):
    """Extract the primary 10-K HTML document from the filing index"""
    response = requests.get(filing_index_url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception("Failed to fetch filing index")

    files = response.json()["directory"]["item"]
    for file in files:
        if file["name"].endswith(".htm") and "10-k" in file["name"].lower():
            return f"{SEC_BASE_URL}/Archives/edgar/data/{file['href']}"

    raise Exception("10-K HTML file not found")

def extract_business_section(ten_k_html_url):
    """Extract the 'Item 1. Business' section from the 10-K HTML page"""
    response = requests.get(ten_k_html_url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception("Failed to fetch 10-K document")

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)  # Extract plain text

    # Find 'Item 1. Business' and stop at 'Item 1A. Risk Factors'
    match = re.search(r"(Item\s*1[\.\s]*Business)(.*?)(Item\s*1A[\.\s]*Risk Factors)", text, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(2).strip()
    else:
        raise Exception("Could not extract Business section from 10-K")

# def get_business_section_from_ticker(ticker):
#     """Master function to extract Business section from 10-K using the ticker symbol"""
#     cik = get_cik_from_ticker(ticker)
#     filing_index_url = get_latest_10k_url(cik)
#     ten_k_html_url = get_10k_html_url(filing_index_url)
#     business_section = extract_business_section(ten_k_html_url)
    
#     return business_section

# # Example Usage
ticker = "AAPL"  # Example: Apple Inc.
# business_info = get_business_section_from_ticker(ticker)
# print(business_info)

cik = get_cik_from_ticker(ticker)

print(cik)
