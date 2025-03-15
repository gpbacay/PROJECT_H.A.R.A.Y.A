import calendar
import logging
import requests
import os
from dotenv import load_dotenv, find_dotenv
import datetime as dt
import geocoder
from threading import Thread
from loading_bar import LoadingBar as loading_bar
import colorama
import sys

class DataScraper:
    def __init__(self) -> None:
        colorama.init(autoreset=True)
        self.loading_bar = loading_bar()

        self.current_time = "."
        self.current_date = "."
        self.current_location = "."
        self.current_weather = "."
        
        self.start_threads()
    
    def start_threads(self):
        # Start a loading bar thread for visual feedback
        tLoadBar4 = Thread(
            target=self.loading_bar.run_loadingbar,
            kwargs={"seconds": 10, "loading_tag": "SCRAPING ONLINE DATA...", "end_tag": "DATA ACQUIRED!"}
        )
        tLoadBar4.start()
        
        t1 = Thread(target=self.initCurrentTime)
        t1.start()

        t2 = Thread(target=self.initCurrentDate)
        t2.start()

        t3 = Thread(target=self.initCurrentLocation)
        t3.start()

        t4 = Thread(target=self.initCurrentWeather)
        t4.start()
        
        tLoadBar4.join()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        
    def initCurrentTime(self):
        currentTime = dt.datetime.now().time()
        Hours = currentTime.hour
        Minutes = currentTime.minute
        if Hours == 0:
            Hours = 12
            time_of_day = "AM"
        elif 0 < Hours < 12:
            time_of_day = "AM"
        elif Hours == 12:
            time_of_day = "PM"
        else:
            Hours = Hours - 12
            time_of_day = "PM"
        if Minutes < 10:
            Minutes = f"0{Minutes}"
        exact_time = f"The current time is {Hours}:{Minutes} {time_of_day}"
        
        time_format = ""
        if int(Minutes) == 0:
            time_format = f"It's {Hours} o'clock."
        elif int(Minutes) < 15 and int(Minutes) != 0:
            time_format = f"It's {Minutes} past {Hours}."
        elif int(Minutes) == 15:
            time_format = f"It's quarter past {Hours}."
        elif int(Minutes) > 15 and int(Minutes) < 30:
            time_format = f"It's {Minutes} past {Hours}."
        elif int(Minutes) == 30:
            time_format = f"It's half past {Hours}."
        elif int(Minutes) > 30 and int(Minutes) < 45:
            time_difference = 60 - int(Minutes)
            time_format = f"It's {time_difference} to {Hours}."
        elif int(Minutes) == 45:
            time_format = f"It's quarter to {Hours}."
        elif int(Minutes) > 45:
            time_difference = 60 - int(Minutes)
            time_format = f"It's {time_difference} to {Hours}."
            
        result = exact_time + " or " + time_format
        self.current_time = result
    
    def initCurrentDate(self):
        current_date = dt.datetime.now()
        Year_number = current_date.year
        Month_number = current_date.month
        Day_number = current_date.day

        def determine_weekday_name(Year_number, Month_number, Day_number):
            day_of_week = calendar.weekday(Year_number, Month_number, Day_number)
            weekday_name = calendar.day_name[day_of_week]
            return weekday_name

        WeekDay_Name = determine_weekday_name(Year_number, Month_number, Day_number)

        def determine_month_name(Month_number):
            month_name = calendar.month_name[Month_number]
            return month_name

        Month_Name = determine_month_name(Month_number)

        result = f"Today is {WeekDay_Name}, {Month_Name} {Day_number}, {Year_number}."
        self.current_date = result

    def initCurrentLocation(self):
        try:
            # Use geocoder to fetch current location via IP address
            g = geocoder.ip('me')
            if g.ok:
                if g.city and g.country:
                    # Store the location as "City, Country" for easier parsing later
                    result = f"{g.city}, {g.country}"
                else:
                    result = "Unknown Location"
                self.current_location = result
            else:
                self.current_location = "Unknown Location"
        except Exception as e:
            self.current_location = "Unknown Location"
            logging.error(f"Error while fetching location data: {e}")

    def initCurrentWeather(self):
        try:
            load_dotenv(find_dotenv())
            BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
            API_KEY = os.environ['WEATHER_API_KEY']

            location_parts = self.getCurrentLocation.split(", ")
            if len(location_parts) >= 2:
                CITY = f"{location_parts[0]}, {location_parts[1]}"
            else:
                CITY = "Santa Cruz, Davao del Sur"
            
            params = {
                'q': CITY,
                'appid': API_KEY,
                'units': 'metric',
            }

            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                weather_data = response.json()

                temperature_celsius = round(weather_data['main']['temp'], 2)
                condition = weather_data['weather'][0]['description']

                formatted_time = dt.datetime.now().strftime('%I:%M %p')
                formatted_date = dt.datetime.now().strftime('%dth of %B %Y')

                result = f"As of {formatted_date}, exactly {formatted_time}, the current weather in {CITY} is {condition}, with a temperature of {temperature_celsius}°C."
                self.current_weather = result
            elif response.status_code == 404:
                CITY = "Santa Cruz, Davao del Sur"
                params['q'] = CITY
                response_default = requests.get(BASE_URL, params=params)
                
                if response_default.status_code == 200:
                    weather_data_default = response_default.json()
                    
                    temperature_celsius_default = round(weather_data_default['main']['temp'], 2)
                    condition_default = weather_data_default['weather'][0]['description']

                    formatted_time_default = dt.datetime.now().strftime('%I:%M %p')
                    formatted_date_default = dt.datetime.now().strftime('%dth of %B %Y')

                    result_default = f"As of {formatted_date_default}, exactly {formatted_time_default}, the current weather in {CITY} is {condition_default}, with a temperature of {temperature_celsius_default}°C."
                    self.current_weather = result_default
                else:
                    self.current_weather = "[Default weather information not available.]"
                    logging.error(f"Error for default city: {response_default.status_code} - {response_default.text}")
            else:
                self.current_weather = "[Current weather information is not available.]"
                logging.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            self.current_weather = "[Current weather information is not available.]"
            logging.error(f"Error while fetching weather data: {e}")

    def getCurrentTime(self):
        self.initCurrentTime()
        return self.current_time
    
    def getCurrentDate(self):
        self.initCurrentDate()
        return self.current_date
    
    def getCurrentLocation(self):
        self.initCurrentLocation()
        return self.current_location
    
    def getCurrentWeather(self):
        return self.current_weather

if __name__ == "__main__":
    Scraper = DataScraper()
    curTime = Scraper.getCurrentTime()
    print(curTime)
    date = Scraper.getCurrentDate()
    print(date)
    location = Scraper.getCurrentLocation()
    print(location)
    weather = Scraper.getCurrentWeather()
    print(weather)
    sys.exit()


# python web_data_scraping_system.py