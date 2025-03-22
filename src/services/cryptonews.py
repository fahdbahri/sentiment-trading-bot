from pygooglenews import GoogleNews


gn = GoogleNews()


CRYPTOS = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple", 
]


def list_sources():

    titles = []
    for crypto in CRYPTOS:
        response = gn.search(crypto, when='12h')
        for r in response['entries']:
            titles.append(r['title'])
    return titles


