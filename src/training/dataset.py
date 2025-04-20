from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import pandas as pd


# set up Database
INFLUX_URL = os.getenv('URL')
TOKEN = os.getenv('ACCESS_TOKEN')
ORG = os.genv('ORG')
BUCKET = os.getenv('BUCKET')



client = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
query_api = client.query_api()



def fetch_historical_data(symbol):

    query = f'''
    from(bucket: "{BUCKET)")
    |> range(start: -30d)
    |> filter(fn: (r) => r["_measurement"] == "crypto_news" and r["symbol"] == "{symbol}")
    |>pivote(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''

    result = query_api.query_data_frame(query)

    return result 


def label_data(df):
    labeled_data = []

    for index, row in df.iterrows():
        current_price = row['price']
        timestamp = parser.parse(row['_time'])

        future_time = timestamp + timedelta(minutes=60)
        query = f'''
        from(bucket: "{BUCKET}")
        |> range(start: {timestamp.isoformat()}, stop: {future_time.isoformat()})
        |> filter(fn: (r) => r["_measurement"] == "crypto_news" and r["symbol"] == "{row['symbol']}")
        |> filter(fn: (r) => r["_field"] == "price")
        |> last()
        '''

        future = query_api.query_data_frame(query)
        if future.empty: continue

        future_price = future.iloc[0]['price']

        change = (future_price - current_price) / current_price

        if change > 0.01:
            label = "buy"
        elif change < -0.01:
            label = "sell"
        else:
            label = "hold"

        labeled_data.append({
           "timestamp": timestamp,
           "title": row['title'],
           "price": current_price,
           "sentiment": row['sentiment_label'],
           "future_price": future_price,
           "label": label,
           "symbol": row['symbol'],
            
        })
    
    return pd.DataFrame(labeled_data)



def generate_dataset(symbols):

    all_dfs = []

    for symbol in symbols:
        df = fetch_historical_data(symbol)
        labeled_df = label_data(df)
        all_dfs.append(labeled_df)

    full_df = pd.concat(all_dfs)
    full_df.to_csv("full_df.csv", index=False)
    print("Data written to file")
