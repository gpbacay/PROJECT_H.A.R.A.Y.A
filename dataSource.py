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
    
    runLoadingBar = LoadingBar.RunLoadingBar

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
        
        result = f"""As of {weather_dayAndTime}, the current weather condition is {weather_condition}, with
        Temperature: {weather_temperature}°C, {weather_precipitation} of precipitation, {weather_humidity} of humidity, 
        and a wind blowing {weather_wind}.
        """
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
    
    #Start Gathering Datas (Initialization Process)
    #Acquire Time
    t1 = Thread(target=SetCurrentTime)
    t1.start()
    tLoadBar1 = Thread(target=runLoadingBar, args=(1, "ACQUIRING TIME DATA", "TIME ACQUIRED!"),)
    tLoadBar1.start()
    tLoadBar1.join()
    #Acquire Date
    t2 = Thread(target=SetCurrentDate)
    t2.start()
    tLoadBar2 = Thread(target=runLoadingBar, args=(1, "ACQUIRING DATE DATA", "DATE ACQUIRED!"),)
    tLoadBar2.start()
    tLoadBar2.join()
    
    #Acquire Location
    tSetLocation = Thread(target=SetCurrentLocation, daemon=True)
    tSetLocation.start()
    tLoadBar3 = Thread(target=runLoadingBar, args=(8, "ACQUIRING LOCATION DATA", "LOCATION ACQUIRED"),)
    tLoadBar3.start()
    tLoadBar3.join()
    
    #Acquire Weather
    tSetWeather = Thread(target=SetCurrentWeather,daemon=True)
    tSetWeather.start()
    tLoadBar4 = Thread(target=runLoadingBar, args=(8, "ACQUIRING WEATHER DATA", "WEATHER ACQUIRED!"),)
    tLoadBar4.start()
    tLoadBar4.join()
    
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