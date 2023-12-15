import calendar
import logging
import requests
import os
from dotenv import load_dotenv, find_dotenv
import datetime as dt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread
from loadingBar import LoadingBar
import colorama
import sys

class DataScraper:
    global current_time, current_date, current_location, current_weather
    # python webDataScrapingSystem.py  
    def __init__(self):
        colorama.init(autoreset=True)
        self.service = Service(ChromeDriverManager(driver_version="120.0.6099.71").install())
        self.runLoadingBar = LoadingBar.RunLoadingBar

        self.current_time = "."
        self.current_date = "."
        self.current_location = "."
        self.current_weather = "."
        
        self.setCurrentTime
        self.setCurrentDate
        self.setCurrentLocation
        self.setCurrentWeather
        
        self.getCurrentTime
        self.getCurrentDate
        self.getCurrentLocation
        self.getCurrentWeather
        
        global initCurrentTime, initCurrentDate, initCurrentLocation, initCurrentWeather
        self.initCurrentTime
        self.initCurrentDate
        self.initCurrentLocation
        self.initCurrentWeather

        self.start_threads()
        
        # LoadingBars
        # tLoadBar = Thread(target=self.runLoadingBar, args=(10, "SCRAPING WEB DATA", "COMPLETED!"),)
        # tLoadBar.start()
        # tLoadBar.join()
        
    
    #_________________________________________________________Setters
    # Run Command: python webDataScrapingSystem.py
    def setCurrentTime(self, currentTime_input: str):
        self.current_time = currentTime_input
        
    def setCurrentDate(self, currentDate_input: str):
        self.current_date = currentDate_input
        
    def setCurrentLocation(self, currentLocation_input: str):
        self.current_location = currentLocation_input
        
    def setCurrentWeather(self, currentWeather_input: str):
        self.current_weather = currentWeather_input
        
    #_________________________________________________________Getters
    # Run Command: python webDataScrapingSystem.py
    def getCurrentTime(self):
        return self.current_time
    
    def getCurrentDate(self):
        return self.current_date
    
    def getCurrentLocation(self):
        return self.current_location
    
    def getCurrentWeather(self):
        return self.current_weather
    
    #_______________________________________________Loading Bar Threads
    # Run Command: python webDataScrapingSystem.py
    def start_threads(self):
        tLoadBar4 = Thread(target=self.runLoadingBar, args=(17, "SCRAPING ONLINE DATA...", "DATA ACQUIRED!"),)
        tLoadBar4.start()
        
        t1 = Thread(target=self.initCurrentTime)
        t1.start()
        t1.join()

        # Acquire Date
        t2 = Thread(target=self.initCurrentDate)
        t2.start()
        t2.join()

        # Acquire Location
        t3 = Thread(target=self.initCurrentLocation)
        t3.start()
        t3.join()

        # Acquire Weather
        t4 = Thread(target=self.initCurrentWeather)
        t4.start()
        t4.join()
        
        tLoadBar4.join()
        
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
        if int(Minutes) == 00:
            time_format = f"It's {Hours} o'clock."
        elif int(Minutes) < 15 and int(Minutes) != 00:
            time_format = f"It's {Minutes} past {Hours}."
        elif int(Minutes) == 15:
            time_format = f"It's quarter past {Hours}."
        elif int(Minutes) > 15 and int(Minutes) < 30:
            time_format = f"It's {Minutes} past {Hours}."
        elif int(Minutes) == 30:
            time_format = f"It's half past {Hours}."
        elif int(Minutes) > 30 and int(Minutes) < 45:
            time_difference = 60 - int(Minutes)
            Minutes = str(time_difference)
            time_format = f"It's {Minutes} to {Hours}."
        elif int(Minutes) == 45:
            time_format = f"It's quarter to {Hours}."
        elif int(Minutes) > 45:
            time_difference = 60 - int(Minutes)
            Minutes = str(time_difference)
            time_format = f"It's {Minutes} to {Hours}."
            
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
            self.driver = webdriver.Chrome(service=self.service)
            self.driver.get("https://www.google.com/search?q=my+current+location")

            city_element = self.driver.find_element(By.CLASS_NAME, "aiAXrc")
            province_element = self.driver.find_element(By.CLASS_NAME, "fMYBhe")
            city = city_element.text
            province = province_element.text

            result = f"You are currently located at: {city}, {province}"

            self.current_location = result
        except Exception as e:
            self.current_location = "[Current location information is not available.]"
            logging.error(f"Error while fetching location data: {e}")
        finally:
            self.driver.quit()

    def initCurrentWeather(self):
        try:
            load_dotenv(find_dotenv())
            # Weather scraping functionality
            BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
            API_KEY = os.environ['WEATHER_API_KEY']

            # Extract the last two parts of the location (city and province)
            location_parts = self.current_location.split(", ")
            if len(location_parts) >= 2:
                CITY = f"{location_parts[-2]}, {location_parts[-1]}, PH"
            else:
                # Provide a default city if the location format is unexpected
                CITY = "Santa Cruz, Davao del Sur, PH"
            
            params = {
                'q': CITY,
                'appid': API_KEY,
                'units': 'metric',  # Use 'imperial' for Fahrenheit
            }

            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                weather_data = response.json()

                temperature_celsius = round(weather_data['main']['temp'], 2)
                condition = weather_data['weather'][0]['description']

                formatted_time = dt.datetime.now().strftime('%I:%M %p')
                formatted_date = dt.datetime.now().strftime('%dth of %B %Y')

                result = f"""As of {formatted_date}, exactly {formatted_time}, the current weather condition at {CITY} is {condition}, with a temperature of {temperature_celsius}°C."""
                self.current_weather = result
            elif response.status_code == 404:
                # City not found, use default city
                CITY = "Santa Cruz, Davao del Sur, PH"
                params['q'] = CITY  # Update the parameters with the default city
                response_default = requests.get(BASE_URL, params=params)
                
                if response_default.status_code == 200:
                    weather_data_default = response_default.json()
                    
                    temperature_celsius_default = round(weather_data_default['main']['temp'], 2)
                    condition_default = weather_data_default['weather'][0]['description']

                    formatted_time_default = dt.datetime.now().strftime('%I:%M %p')
                    formatted_date_default = dt.datetime.now().strftime('%dth of %B %Y')

                    result_default = f"""As of {formatted_date_default}, exactly {formatted_time_default}, the current weather condition at {CITY} is {condition_default}, with a temperature of {temperature_celsius_default}°C."""
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



if __name__ == '__main__':
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

# python webDataScrapingSystem.py