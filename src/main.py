from services.cryptonews import *
from services.bot_sentiment import *



def main():
    news_data = list_sources()

    get_sentiment_score(news_data)


if __name__ == "__main__":
    main()



