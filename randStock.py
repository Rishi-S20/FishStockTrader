import requests
import random


def getRandStock ():

    url = "https://dumbstockapi.com/stock?format=tickers-only&exchange=NYSE"


    response = requests.get(url)

    data = response.json()
    return (random.choice(data))  


