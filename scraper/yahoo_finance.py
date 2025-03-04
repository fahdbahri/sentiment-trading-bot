import requests
from bs4 import BeautifulSoup




def scrape_yahoo_finance():
    try:

        url = "https://finance.yahoo.com/topic/stock-market-news/"

        print(f"Scraping {url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom             e/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news = soup.find_all("div", class_="topic-stories yf-sz4j54")
            print(news)

    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    scrape_yahoo_finance()
