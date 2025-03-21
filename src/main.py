from services.scrape_sources import *
from services.bot_sentiment import *



def main():
    news_data = scrape_news()

    get_sentiment_score(news_data)


if __name__ == "__main__":
    main()



