import datetime
import calendar
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread
from LoadingBar import LoadingBar
import time
    
class dataSource():
    global current_date, current_time, current_location, current_weather
    current_time = ""
    current_date = ""
    current_location = ""
    current_weather = ""

    def SetCurrentTime():
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
        global current_time
        current_time = result
    
    def SetCurrentDate():
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
        global current_date
        current_date = result
        time.sleep(0.5)

    def SetCurrentLocation():
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.google.com/search?q=my+current+location")
        element1 = driver.find_element(By.CLASS_NAME, "aiAXrc")
        element2 = driver.find_element(By.CLASS_NAME, "fMYBhe")
        city = element1.text
        province = element2.text
        result = city + ", " + province
        global current_location
        current_location = result
        driver.quit()
    
    def SetCurrentWeather():
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.google.com/search?q=current+location+weather")
        element1 = driver.find_element("id", "wob_dc")
        element2 = driver.find_element("id", "wob_tm")
        weather_condition = element1.text
        weather_temperature = element2.text
        result = "The current weather is " + weather_condition + ", " + "Temperature: " + weather_temperature + "°C"
        global current_weather
        current_weather = result
        driver.quit()
    
    def GetCurrentTime():
        return current_time
    
    def GetCurrentDate():
        return current_date
    
    def GetCurrentLocation():
        return current_location
    
    def GetCurrentWeather():
        return current_weather
    
    #Acquire Time
    t1 = Thread(target=SetCurrentTime)
    t1.start()
    
    #Acquire Date
    t2 = Thread(target=SetCurrentDate)
    t2.start()
    
    #Acquire Location
    tSetLocation = Thread(target=SetCurrentLocation)
    tSetLocation.start()
    tLoadLocation = Thread(target=LoadingBar, args=(8, "Acquiring location data", "Location acquired",))
    tLoadLocation.start()
    tLoadLocation.join()
    
    time.sleep(1)
    #Acquire Weather
    tSetWeather = Thread(target=SetCurrentWeather)
    tSetWeather.start()
    tLoadWeather = Thread(target=LoadingBar, args=(8, "Acquiring weather data", "Weather acquired",))
    tLoadWeather.start()
    tSetWeather.join()
    
if __name__ == '__main__':
    date = dataSource.GetCurrentDate()
    print(date)
    curTime = dataSource.GetCurrentTime()
    print(curTime)
    location = dataSource.GetCurrentLocation()
    print(location)
    weather = dataSource.GetCurrentWeather()
    print(weather)
#______________python dataSource.py