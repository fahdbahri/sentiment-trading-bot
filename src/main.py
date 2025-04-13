from services.cryptonews import *
from services.bot_sentiment import *
import schedule



def main():
    news_data = list_sources()
    get_sentiment_score(news_data)



schedule.every(12).hours.do(main)

while True:
    schedule.run_pending()
    time.sleep(60)


