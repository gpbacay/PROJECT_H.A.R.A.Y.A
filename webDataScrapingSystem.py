import sys
import datetime
import calendar
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread
from loadingBar import LoadingBar
import colorama

class DataScraper:  
    # python webDataScrapingSystem.py  
    def __init__(self):
        colorama.init(autoreset=True)
        self.service = Service(ChromeDriverManager(driver_version="118.0.5993.89").install())
        self.driver = webdriver.Chrome(service=self.service)
        self.runLoadingBar = LoadingBar.RunLoadingBar
        
        self.current_time = "."
        self.current_date = "."
        self.current_location = "."
        self.current_weather = "."
        self.start_threads()
        
        # LoadingBars
        # tLoadBar = Thread(target=self.runLoadingBar, args=(10, "SCRAPING WEB DATA", "COMPLETED!"),)
        # tLoadBar.start()
        # tLoadBar.join()
        
        tLoadBar1 = Thread(target=self.runLoadingBar, args=(0.1, "ACQUIRING TIME DATA", "TIME ACQUIRED!"),)
        tLoadBar1.start()
        tLoadBar1.join()
        
        tLoadBar2 = Thread(target=self.runLoadingBar, args=(0.1, "ACQUIRING DATE DATA", "DATE ACQUIRED!"),)
        tLoadBar2.start()
        tLoadBar2.join()
        
        tLoadBar3 = Thread(target=self.runLoadingBar, args=(0.1, "ACQUIRING LOCATION DATA", "LOCATION ACQUIRED"),)
        tLoadBar3.start()
        tLoadBar3.join()
        
        tLoadBar4 = Thread(target=self.runLoadingBar, args=(0.1, "ACQUIRING WEATHER DATA", "WEATHER ACQUIRED!"),)
        tLoadBar4.start()
        tLoadBar4.join()
    
    #_______________________________________________Loading Bar Threads
    # Run Command: python webDataScrapingSystem.py
    def start_threads(self):
        t1 = Thread(target=self.initCurrentTime)
        t1.start()
        
        # Acquire Date
        t2 = Thread(target=self.initCurrentDate)
        t2.start()
        
        # Acquire Location
        tSetLocation = Thread(target=self.initCurrentLocation)
        tSetLocation.start()
        
        # Acquire Weather
        tSetWeather = Thread(target=self.initCurrentWeather)
        tSetWeather.start()
        
    def initCurrentTime(self):
        currentTime = datetime.datetime.now().time()
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
        self.setCurrentTime(result)
    
    def initCurrentDate(self):
        current_date = datetime.datetime.now()
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
        self.setCurrentDate(result)

    def initCurrentLocation(self):
        try:
            self.driver.get("https://www.google.com/search?q=my+current+location")
            
            city_element = self.driver.find_element(By.CLASS_NAME, "aiAXrc")
            province_element = self.driver.find_element(By.CLASS_NAME, "fMYBhe")
            city = city_element.text
            province = province_element.text
            
            result = "You are currently located at: " + city + ", " + province
            
            self.setCurrentLocation(result)
        except Exception as e:
            self.setCurrentLocation("[Current location information is not available.]")
            print(f"\nCurrent location information is not available: {e}\n")
        finally:
            self.driver.quit()
    
    def initCurrentWeather(self):
        try:
            self.driver.get("https://www.google.com/search?q=current+weather")
            
            dayAndTime_element = self.driver.find_element("id", "wob_dts")
            condition_element = self.driver.find_element("id", "wob_dc")
            temperature_element = self.driver.find_element("id", "wob_tm")
            precipitation_element = self.driver.find_element("id", "wob_pp")
            humidity_element = self.driver.find_element("id", "wob_hm")
            wind_element = self.driver.find_element("id", "wob_ws")
            
            weather_dayAndTime = dayAndTime_element.text
            weather_condition = condition_element.text
            weather_temperature = temperature_element.text
            weather_precipitation = precipitation_element.text
            weather_humidity = humidity_element.text
            weather_wind = wind_element.text
            
            result = f"""
            As of {weather_dayAndTime}, the current weather condition at your current location is {weather_condition}, 
            with a temperature of {weather_temperature}°C, {weather_precipitation} of precipitation, {weather_humidity} of humidity, 
            and a wind blowing {weather_wind}.
            """
            self.setCurrentWeather(result)
        except Exception as e:
            self.setCurrentWeather("[Current weather information is not available.]")
            print(f"\nCurrent weather information is not available: {e}\n")
        finally:
            self.driver.quit()
    
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
    def GetCurrentTime(self):
        return self.current_time
    
    def GetCurrentDate(self):
        return self.current_date
    
    def GetCurrentLocation(self):
        return self.current_location
    
    def GetCurrentWeather(self):
        return self.current_weather

if __name__ == '__main__':
    Scraper = DataScraper()
    curTime = Scraper.GetCurrentTime()
    print(curTime)
    date = Scraper.GetCurrentDate()
    print(date)
    location = Scraper.GetCurrentLocation()
    print(location)
    weather = Scraper.GetCurrentWeather()
    print(weather)
    sys.exit()

# python webDataScrapingSystem.py