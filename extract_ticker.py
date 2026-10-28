import os
import time 
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("POLYGON_API_KEY")
# print(API_KEY)

LIMIT = 1000

url = f"https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"

def extract_tickers():
    """
        Extracts all stock tickers using massive api and stores in the data folder with the name all_stock_tickers.csv
    """
    all_ticker = []
    next_url = url 
    count = 0

    while next_url:
        count += 1
        print(f"Fetching: {next_url[:70]}..., {count}")
        response = requests.get(next_url)
        response.raise_for_status()
        ticker_json = response.json()

        all_ticker.extend(ticker_json['results'])
        print(f'Fetched {len(ticker_json['results'])} tickers, tickers so far: {len(all_ticker)}')

        raw_url = ticker_json.get('next_url')

        if raw_url:
            next_url = f"{raw_url}&apikey={API_KEY}"
            # Rate limit: 5 requests/min = 1 request every 12 seconds
            print("Sleeping 12 seconds to respect free tier rate limit...")
            time.sleep(12)
        else:
            next_url = None
        # break


    df = pd.DataFrame(all_ticker)
    print(f"Completed! Total tickers: {len(df)}")

    df.to_csv('data/all_stock_tickers.csv')

df.info()
df[df['active'] == True]

df.describe().T