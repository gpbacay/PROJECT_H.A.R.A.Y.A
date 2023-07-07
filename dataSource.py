import datetime
import calendar
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
    
class dataSource():
    def GetCurrentDate():
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
        
        current_date = "Today is " + WeekDay_Name + ", " + Month_Name + " " + str(Day_number) + ", " + str(Year_number)
        return current_date

    def GetCurrentTime():
        current_time = datetime.datetime.now().time()
        Hours = current_time.hour
        Minutes = current_time.minute
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
        
        current_time = f"The current time is {Hours}:{Minutes} {time_of_day}"
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
        current_time = current_time + " or should I say, " + time_format
        return current_time

    def GetCurrentLocation():
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.google.com/search?q=my+current+location")
        element1 = driver.find_element(By.CLASS_NAME, "aiAXrc")
        element2 = driver.find_element(By.CLASS_NAME, "fMYBhe")
        text1 = element1.text
        text2 = element2.text
        current_location = text1 + ", " + text2
        driver.quit()
        return current_location
    
    def GetCurrentWeather():
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.google.com/search?q=current+location+weather")
        element1 = driver.find_element("id", "wob_dc")
        element2 = driver.find_element("id", "wob_tm")
        text1 = element1.text
        text2 = element2.text
        current_weather = "It is currently " + text1 + ", " + "Temperature: " + text2 + "°C"
        driver.quit()
        return current_weather
    
if __name__ == '__main__':
    dataSource()
    #print(timeStamp.GetCurrentTime())
    #print(timeStamp.GetCurrentDate())
#______________python dataSource.py