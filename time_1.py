import pyttsx3
import datetime

engine = pyttsx3.init()

# Get the current time
current_time = datetime.datetime.now()
hour = current_time.hour
minute = current_time.minute

# Convert the hour to 12-hour format
if hour == 0:
    hour = 12
elif hour > 12:
    hour -= 12

minute = 00
# Convert the current time to text
if minute == 30:
    time_text = "quarter to " + str(hour)
elif minute == 00:
    time_text = f"It's {hour} o'clock"
    print(time_text)
else:
    time_text = f"{hour} {minute}"

# Speak the current time
engine.say(time_text)
engine.runAndWait()

#Run command: python time.py