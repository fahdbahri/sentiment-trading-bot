from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from influxdb import influxDBClient, Point, WritePrecision
from datetime import datetime
import os

load_dotenv()

# set up Database
INFLUX_URL = 'http://localhost:8086'
TOKEN = os.getenv('ACCESS_TOKEN')
ORG = 'fahd_org'
BUCKET = 'crypto'


# connect to database
client = influxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


def store_new(news_title, price, symbol, sentiment_score, sentiment_label):

    point = Point("crypto_news") \
            .tag("symbol", symbol) \
            .tag("title", news_title) \
            .field("price", price) \
            .field("sentiment_score", sentiment_score) \
            .field("sentiment_label", sentiment_label) \
            .time(datetiem.utcnow())

    print("Data written to database")
            

    write_api.write(bucket=BUCKET, record=point)

def pipeline_method(payload):

    tokenizer = AutoTokenizer.from_pretrained('prosusAI/finbert')
    model = AutoModelForSequenceClassification.from_pretrained('prosusAI/finbert')

    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
    results = classifier(payload)

    return results[0]


def get_sentiment_score(news_data):

    for news in news_data:

        title = news['title']
        price = news['price']
        symbol = news['symbol']
        


        output = pipeline_method(news)

        sentiment_label = output['label']
        sentiment_score = output['score']

        # write to database
        store_new(title, price, symbol, sentiment_score, sentiment_label)



