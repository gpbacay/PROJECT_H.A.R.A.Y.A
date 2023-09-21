import psutil
import colorama
colorama.init(autoreset=True)

battery = psutil.sensors_battery()
percentage = colorama.Fore.GREEN + str(battery.percent)
#isCharging = battery.power_plugged
response = f"The current battery percentage is " + str(percentage) + "%"
print(response) 



#_________python test26.py