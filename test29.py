import datetime as dt
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.environ['WEATHER_API_KEY']
CITY = "Davao City"
url = BASE_URL + "apiid=" + API_KEY + "&q=" + CITY

response = requests.get(url=url).json()
print(response)

#__________python test29.py