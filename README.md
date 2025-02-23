# Company-Researcher

## Form 10-K Extractor & Summarizer
> This repository contains code for extracting and summarizing the Business Section (Item 1) from the latest 10-K filings of publicly traded companies. Using the SEC API, the script fetches the most recent 10-K filing based on a given ticker symbol, identifies and extracts the relevant business information, and summarizes it using Gemini. The output is stored in a structured directory for easy access.

## Folder information
📂 URLS
- Contains the URLs of the form 10-k stored in the EDGAR database. Extracted based on their ticker symbol.

📂 Business section
- Contains the Business section of the company the user searched for.

📂 AI Summary
- Contains the Summary based on the information extracted an stored in Business section

## Motivation
**Use Cases**
- Quickly analyzing a company's business model and operations from its latest 10-K filing.
- Automating the extraction and summarization of financial documents for research or investment analysis
- Reducing the manual effort in processing regulatory filings for competitive analysis
   
Future Scope
- Enhancing the extraction process to improve accuracy when identifying the business section.
- Supporting additional sections of the 10-K, such as risk factors or management discussion.
- Expanding the summarization capabilities with more structured outputs, including key highlights and comparisons.
- Integrating a web interface or API for real-time querying and report generation
