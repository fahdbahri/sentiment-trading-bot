from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta 
from dateutil.parser import parse

load_dotenv()

# set up Database
INFLUX_URL = os.getenv('URL')
TOKEN = os.getenv('ACCESS_TOKEN')
ORG = os.getenv('ORG')
BUCKET = os.getenv('BUCKET')



client = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
query_api = client.query_api()



def fetch_historical_data(symbol):
     
    health = client.health()
    if health.status == "pass":
        print("Database is healthy")
    else:
        print("Database is not healthy")

    try:

        query = f'''
        from(bucket: "{BUCKET}")
        |> range(start: -7d)
        |> filter(fn: (r) => r["_measurement"] == "crypto_news" and r["symbol"] == "{symbol}")
        |>pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''

        result = query_api.query_data_frame(query)

        return result 
    except Exception as e:
        print(f"An error occurred while fetching historical data: {e}")



def label_data(df):


    try:

        labeled_data = []

        for index, row in df.iterrows():
            current_price = float(row['price'])
            print(current_price)
            timestamp = row['_time']

            future_time = timestamp + timedelta(minutes=60)
            query = f'''
            from(bucket: "{BUCKET}")
            |> range(start: {timestamp.isoformat()}, stop: {future_time.isoformat()})
            |> filter(fn: (r) => r["_measurement"] == "crypto_news" and r["symbol"] == "{row['symbol']}")
            |> filter(fn: (r) => r["_field"] == "price")
            |> last()
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            '''

            future = query_api.query_data_frame(query)
            if future.empty: continue

            future_price = float(future.iloc[0]['price'])
            
            change = (future_price - current_price) / (current_price)

            print(future_price)
            print(current_price)
            print(change)

            

            if change > 0.0002:
                label = "buy"
            elif change < -0.0002:
                label = "sell"
            else:
                label = "hold"
            print(label)

            hour_of_day = timestamp.hour
            day_of_week = timestamp.weekday()

            labeled_data.append({
            "timestamp": timestamp,
            "title": row['title'],
            "price": current_price,
            "sentiment": row['sentiment_label'],
            "sentiment_score": row['sentiment_score'],
            "future_price": future_price,
            "label": label,
            "symbol": row['symbol'],
            "hour_of_day": hour_of_day,
            "day_of_week": day_of_week,
            
            })
        return pd.DataFrame(labeled_data)
    except Exception as e:
        print(f"An error occurred while labeling data: {e}")




def generate_dataset(symbols):

    try:

        all_dfs = []

        for symbol in symbols:
            df = fetch_historical_data(symbol)
            labeled_df = label_data(df)
            all_dfs.append(labeled_df)

        full_df = pd.concat(all_dfs)
        full_df.to_csv("full_df.csv", mode="a", index=False, header=False)
        print("Data written to file")

    except Exception as e:
        print(f"An error occurred while generating dataset: {e}")





