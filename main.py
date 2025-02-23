import os
from Extract import get_latest_10k_url, extract_business_section
from openai import OpenAI 
import os
from dotenv import load_dotenv
load_dotenv()

load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = os.getenv("openrouter_api_key")
)

def call_ai_summarizer(business_text):
    """Send the extracted 10-K Business section to LLM and get a summary"""
    
    system_prompt = "You are a business analyst summarizing information from 10-K filings. Provide a concise and structured summary of the business section."
    
    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-preview-02-05:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": business_text}
        ]
    )

    summary = response.choices[0].message.content
    return summary

def main():
    ticker = input("Enter the ticker symbol: ").strip().upper()  # Example: AAPL, KO, TSLA
    
    try:
        filing_url = get_latest_10k_url(ticker)
        business_section = extract_business_section(filing_url, ticker)
        
        summary = call_ai_summarizer(business_section)

        # Ensure directory exists
        os.makedirs("AI-10k-summaries", exist_ok=True)

        # Save summary to a file
        summary_path = os.path.join("AI-10k-summaries", f"{ticker}_summary.txt")
        with open(summary_path, "w", encoding="utf-8") as file:
            file.write(summary)

        print(f"\n*** Summary saved to {summary_path}***")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
