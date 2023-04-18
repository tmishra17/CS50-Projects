import requests
import key
from flask import render_template
def get_results(search_input, country_code):
    url = "https://amazon-price1.p.rapidapi.com/search"

    querystring = {"keywords":search_input,"marketplace":country_code}

    headers = {
        "X-RapidAPI-Key": key.API_KEY,
        "X-RapidAPI-Host": "amazon-price1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring) # search results page
    return response.json()

def error(message, errnum=400):
    return render_template("error.html",message=message, errnum=errnum)

