import os
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

def scrape_business_insider():
    try:
        all_news_data = []
 
        print("Loading sources from business insider...")

        url = "https://markets.businessinsider.com/stocks"

        # Add a User-Agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom             e/91.0.4472.124 Safari/537.36"
        }

        # Make the request with headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('section', class_="popular-articles")
            stocks_news = soup.find_all("section", class_="instrument-stories")
            for stock in stocks_news:
                all_news_data.append(stock.text)
            for article in articles:
                all_news_data.append(article.text)
            print(all_news_data)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

        # Add a delay to avoid too many requests
        time.sleep(2) 

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_business_insider()

    






