import datetime
import calendar

class timeStamp():
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
        return current_time

if __name__ == '__main__':
    timeStamp()
    #print(timeStamp.GetCurrentTime())
    #print(timeStamp.GetCurrentDate())
#______________python timeStamp.py