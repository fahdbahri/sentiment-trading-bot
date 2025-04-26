from services.cryptonews import *
from services.bot_sentiment import *
from training.dataset import *
import schedule
import time



def main():
    symbols = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "XRPUSDT"]
    

    print("Running...")
    news_data = list_sources()
    print("Data fetched")
    get_sentiment_score(news_data)
    print("Data sent to database")
    print("loading the data into csv file")
    generate_dataset(symbols)



schedule.every(12).hours.do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
