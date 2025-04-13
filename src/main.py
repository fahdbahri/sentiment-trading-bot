from services.cryptonews import *
from services.bot_sentiment import *
import schedule
import time



def main():
    print("Running...")
    news_data = list_sources()
    print("Data fetched")
    get_sentiment_score(news_data)
    print("Data sent to database")



schedule.every(12).hours.do(main)

while True:
    schedule.run_pending()
    time.sleep(60)


