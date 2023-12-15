import requests
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = os.environ['WEATHER_API_KEY']
CITY = "Tampakan, South Cotabato, PH"

def get_weather(api_key, city):
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Use 'imperial' for Fahrenheit
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

def convert_timestamp_to_readable(timestamp, timezone):
    return datetime.utcfromtimestamp(timestamp + timezone).strftime('%Y-%m-%d %I:%M:%S %p')

def print_important_details(weather_data):
    # Convert temperature to Celsius explicitly
    temperature_celsius = round(weather_data['main']['temp'], 2)
    feels_like_celsius = round(weather_data['main']['feels_like'], 2)

    # Convert timestamps to readable format
    sunrise_time = convert_timestamp_to_readable(weather_data['sys']['sunrise'], weather_data['timezone'])[11:]
    sunset_time = convert_timestamp_to_readable(weather_data['sys']['sunset'], weather_data['timezone'])[11:]
    current_time = convert_timestamp_to_readable(weather_data['dt'], weather_data['timezone'])

    formatted_details = f"Location: {CITY}\n" \
                        f"Country: {weather_data['sys']['country']}\n" \
                        f"Coordinates: {weather_data['coord']['lat']}, {weather_data['coord']['lon']}\n" \
                        f"Weather: {weather_data['weather'][0]['description']}\n" \
                        f"Temperature: {temperature_celsius}°C\n" \
                        f"Feels Like: {feels_like_celsius}°C\n" \
                        f"Humidity: {weather_data['main']['humidity']}%\n" \
                        f"Wind Speed: {weather_data['wind']['speed']} m/s\n" \
                        f"Sunrise Time: {sunrise_time}\n" \
                        f"Sunset Time: {sunset_time}\n" \
                        f"Current Date: {current_time.split()[0]}\n" \
                        f"Current Time: {current_time.split()[1]}"

    print(formatted_details)

def main():
    weather_data = get_weather(API_KEY, CITY)

    if weather_data:
        print_important_details(weather_data)
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()


#__________python test29.py