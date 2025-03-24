from pygooglenews import GoogleNews
import requests


gn = GoogleNews()


CRYPTOS = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple", 
]


def list_sources():

    crypto_data = []
    

    

    
    for crypto in CRYPTOS:
        price, symbol = get_price(crypto)
        response = gn.search(crypto, when='12h')
        for r in response['entries']:
            
            titles = {
                    "title": r['title'],
                    "price": price,
                    "symbol": symbol,

                    }
            crypto_data.append(titles)



    print(crypto_data)




def get_price(crypto):

    if crypto == "bitcoin":
        
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        response = requests.get(url).json()

        return response['price'], response['symbol']

    elif crypto == "ethereum":
        
        url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

        response = requests.get(url).json()

        return response['price'], response['symbol']
    elif crypto == "litecoin":
        
        url = "https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT"

        response = requests.get(url).json()

        return response['price'], response['symbol']
        
    elif crypto == "ripple":
        
        url = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"

        response = requests.get(url).json()

        return response['price'], response['symbol']
        


      
    

