import requests
from bs4 import BeautifulSoup
import datetime


def scrape_yahoo_finance(date):
    try:

        all_news_data = []

        url = "https://finance.yahoo.com/topic/stock-market-news/"

        print(f"Scraping {url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom             e/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news = soup.find_all("div", class_="topic-stream")
            
            
            # printing news articles
            for i, news_article in enumerate(news):
                articles_tags = news_article.find_all("div", class_="content yf-82qtw3")
                for article in articles_tags:
                    title = article.find("h3").text
                    content = article.find("p").text
                    

            
                    news_data = {
                        "source": "Yahoo Finance",
                        "title": title,
                        "content": content,
                        "sentiment_score": None,
                        "published_at": date
                        }
                    all_news_data.append(news_data)
            
            
            print(all_news_data)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")


    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    date = datetime.datetime.now()
    scrape_yahoo_finance(date)
