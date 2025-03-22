import os
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import spacy
import yfinance as yf


# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Stock symbol mapping
STOCK_MAPPING = {
    "Tesla": "TSLA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Google": "GOOGL",
    "Meta": "META",
}


def extract_stock_symbol(news_title):
    # Try matching known stock names
    for company, symbol in STOCK_MAPPING.items():
        if company.lower() in news_title.lower():
            return symbol

    # Try extracting company name with NLP
    doc = nlp(news_title)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return STOCK_MAPPING.get(ent.text, None)  # Convert to symbol if found

    return None

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return price
    except:
        return None

def scrape_news():
    all_news_data = []

    # Scrape Yahoo Finance
    try:
        print("Scraping Yahoo Finance...")
        url = "https://finance.yahoo.com/topic/stock-market-news/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("SUccessfully fetched data from Yahoo Finance")
            soup = BeautifulSoup(response.text, 'html.parser')
            news = soup.find_all("div", class_="topic-stream")
            
            
            for i, news_article in enumerate(news):
                articles_tags = news_article.find_all("div", class_="content yf-82qtw3")
                for article in articles_tags:
                    title = article.find("h3").text
                    content = article.find("p").text
                    formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                    stock_symbol = extract_stock_symbol(content)

                    if stock_symbol:
                        price = get_stock_price(stock_symbol)

                        print(f"title: {title}")
                        print(f"Stock price: {price}")
                        print(f"Stock symbol: {stock_symbol}")
                    else:
                        print(f"Stock symbol not found for {title}")

                    news_data = {
                        "source": "Yahoo Finance",
                        "title": title,
                        "content": content,
                        "sentiment_score": None,
                        "published_at": formatted_date
                    }
                    all_news_data.append(news_data)

                    print("Finshed scraping Yahoo Finance")
        else:
            print(f"Failed to fetch data from Yahoo Finance. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while scraping Yahoo Finance: {e}")

    # Scrape Business Insider
    try:
        print("Scraping Business Insider...")
        url = "https://markets.businessinsider.com/stocks"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('section', class_="popular-articles")
            stocks_news = soup.find_all("div", class_="instrument-stories__story")

            for stock_news in stocks_news:
                title = stock_news.find("h3", class_="instrument-stories__title")
                date_time = stock_news.find("time", class_="instrument-stories__date").get("datetime")
                article_url_tag = stock_news.find("a", class_="instrument-stories__link")

                if article_url_tag:
                    article_url = f"https://markets.businessinsider.com{article_url_tag['href']}"
                    articles_response = requests.get(article_url, headers=headers)
                    if articles_response.status_code == 200:
                        articles_soup = BeautifulSoup(articles_response.text, 'html.parser')
                        article_content = articles_soup.find("section", class_="post-content typography")

                        news_data = {
                            "source": "Business Insider",
                            "title": title.text.strip(),
                            "content": article_content.text.strip(),
                            "sentiment_score": None,
                            "published_at": date_time
                        }
                        all_news_data.append(news_data)
                        print("Finished scraping Business Insider")
                    else:
                        print(f"Failed to fetch article: {title.text.strip()}")
                else:
                    print(f"Failed to fetch article: {title.text.strip()}")

            for i, article in enumerate(articles):
                for data in article.find_all("div", class_="popular-articles__story"):
                    current_date_time = data.find("time", class_="popular-articles__date").get("datetime")
                    title = data.find("h3", class_="popular-articles__title").text.strip()
                    article_url_tag = data.find("a", class_="popular-articles__link")
                    article_url = f"https://markets.businessinsider.com{article_url_tag['href']}"

                    if article_url:
                        articles_response = requests.get(article_url, headers=headers)
                        if articles_response.status_code == 200:
                            articles_soup = BeautifulSoup(articles_response.text, 'html.parser')
                            article_content = articles_soup.find("section", class_="post-content typography")
                            news_data = {
                                "source": "Business Insider",
                                "title": title,
                                "content": article_content.text.strip(),
                                "sentiment_score": None,
                                "published_at": current_date_time
                            }
                            all_news_data.append(news_data)
                            print("Finished scraping Business Insider 2")
                        else:
                            print(f"Failed to fetch article: {title}")
                    else:
                        print(f"Failed to fetch article: {title}")

        else:
            print(f"Failed to fetch data from Business Insider. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while scraping Business Insider: {e}")

    return all_news_data

if __name__ == "__main__":
    news_data = scrape_news()
    print(news_data)
