import datetime
import calendar
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread
from loadingBar import LoadingBar
import colorama

class DataScrapper:    
    def __init__(self):
        print(colorama.Fore.GREEN + "Scraping data out from the internet...")
        colorama.init(autoreset=True)
        self.service = Service(ChromeDriverManager(driver_version="117.0.5938.92").install())
        self.runLoadingBar = LoadingBar.RunLoadingBar
        self.current_time = ""
        self.current_date = ""
        self.current_location = ""
        self.current_weather = ""
        self.start_threads()
        
        # LoadingBars
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
        
    def start_threads(self):
        t1 = Thread(target=self.SetCurrentTime)
        t1.start()
        
        # Acquire Date
        t2 = Thread(target=self.SetCurrentDate)
        t2.start()
        
        # Acquire Location
        tSetLocation = Thread(target=self.SetCurrentLocation)
        tSetLocation.start()
        
        # Acquire Weather
        tSetWeather = Thread(target=self.SetCurrentWeather)
        tSetWeather.start()
        
    def SetCurrentTime(self):
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
            
        result = exact_time + " or should I say, " + time_format
        self.current_time = result
    
    def SetCurrentDate(self):
        Dates = []
        Date_format = datetime.datetime.now().strftime("%m/%d/%y")
        Date_format = Date_format.replace('/', ' ')
        Date_format = Date_format.split(' ')
        Dates.append(Date_format)
        
        Year_number = Dates[-1][2]
        Year_number = int(Year_number) + 2000
        
        Month_number = Dates[-1][0][-1]
        Month_number = int(Month_number)
        
        Day_number = Dates[-1][1]
        Day_number = int(Day_number)
        
        def determine_weekday_name(Year_number, Month_number, Day_number):
            day_of_week = calendar.weekday(Year_number, Month_number, Day_number)
            weekday_name = calendar.day_name[day_of_week]
            return weekday_name
        WeekDay_Name = determine_weekday_name(Year_number, Month_number, Day_number)
        
        def determine_month_name(Month_number):
            month_name = calendar.month_name[Month_number]
            return month_name
        Month_Name = determine_month_name(Month_number)
        
        result = "Today is " + WeekDay_Name + ", " + Month_Name + " " + str(Day_number) + ", " + str(Year_number)
        self.current_date = result

    def SetCurrentLocation(self):
        try:
            driver = webdriver.Chrome(service=self.service)
            driver.get("https://www.google.com/search?q=my+current+location")
            city_element = driver.find_element(By.CLASS_NAME, "aiAXrc")
            province_element = driver.find_element(By.CLASS_NAME, "fMYBhe")
            city = city_element.text
            province = province_element.text
            result = "You are currently located at: " + city + ", " + province
            self.current_location = result
        except Exception as e:
            self.current_location = "[Current location information is not available.]"
            print(f"Current location information is not available: {e}")
        finally:
            driver.quit()
    
    def SetCurrentWeather(self):
        try:
            location = self.current_location
            location = location.split(":")
            location = location[-1]
            driver = webdriver.Chrome(service=self.service)
            driver.get("https://www.google.com/search?q=current+weather+in+" + location)
            
            dayAndTime_element = driver.find_element("id", "wob_dts")
            condition_element = driver.find_element("id", "wob_dc")
            temperature_element = driver.find_element("id", "wob_tm")
            precipitation_element = driver.find_element("id", "wob_pp")
            humidity_element = driver.find_element("id", "wob_hm")
            wind_element = driver.find_element("id", "wob_ws")
            
            weather_dayAndTime = dayAndTime_element.text
            weather_condition = condition_element.text
            weather_temperature = temperature_element.text
            weather_precipitation = precipitation_element.text
            weather_humidity = humidity_element.text
            weather_wind = wind_element.text
            
            result = f"""
            As of {weather_dayAndTime}, the current weather condition at {location} is {weather_condition}, 
            with a temperature of {weather_temperature}°C, {weather_precipitation} of precipitation, {weather_humidity} of humidity, 
            and a wind blowing {weather_wind}.
            """
            self.current_weather = result
        except Exception as e:
            self.current_weather = "[Current weather information is not available.]"
            print(f"Current weather information is not available: {e}")
        finally:
            driver.quit()
    
    def GetCurrentTime(self):
        return self.current_time
    
    def GetCurrentDate(self):
        return self.current_date
    
    def GetCurrentLocation(self):
        return self.current_location
    
    def GetCurrentWeather(self):
        return self.current_weather

if __name__ == '__main__':
    Scrapper = DataScrapper()
    curTime = Scrapper.GetCurrentTime()
    print(curTime)
    date = Scrapper.GetCurrentDate()
    print(date)
    location = Scrapper.GetCurrentLocation()
    print(location)
    weather = Scrapper.GetCurrentWeather()
    print(weather)

# python webDataScrapingSystem.py