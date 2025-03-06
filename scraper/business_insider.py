import os
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
            # Latest news
            articles = soup.find_all('section', class_="popular-articles")
           
            # Stocks news
            stocks_news = soup.find_all("section", class_="instrument-stories")

            articles_urls = []
            for i, article in enumerate(articles):

                for data in article.find_all("div", class_="popular-articles__story"):
                    dattime = data.find("time", class_="popular-articles__date").get("datetime")
                    title = data.find("h3", class_="popular-articles__title").text.strip()
                    article_url_tag = data.find("a", class_="popular-articles__link")
                    article_url = f"https://markets.businessinsider.com{article_url_tag['href']}"

                    if article_url:
                        print("article_url\n", article_url)
                        articles_response= requests.get(article_url, headers=headers)
                        if articles_response.status_code == 200:
                            
                            articles_soup = BeautifulSoup(articles_response.text, 'html.parser')
                            article_content = articles_soup.find("section", class_="post-content typography") 
                        else:
                            print(f"Failed to fetch article: {title}")


                        news_data = {
                                "source": "Business Insider",
                                "title": title,
                                "content": article_content.text,
                                "sentiment_score": None,
                                "published_at": dattime
                                }
                        

                    else:
                        print(f"Failed to fetch article: {title}")

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}") 

    except Exception as e:
        print(f"An error occurred: {e}")




    





