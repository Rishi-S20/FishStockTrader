import requests


def getRandStock ():

    url = "https://random-stocks-api.p.rapidapi.com/api/random-stocks"

    headers = {
        "x-rapidapi-key": "67e2ef61d6msha2b4e4e13420b83p196858jsn2ed01aef0731",
        "x-rapidapi-host": "random-stocks-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return (data["stocks"])  


