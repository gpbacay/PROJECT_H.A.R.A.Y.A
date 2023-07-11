import json
from urllib.request import urlopen

def get_current_location():
    url="http://ipinfo.io/json"
    response=urlopen(url=url)
    data=json.load(response)
    return data

if __name__ == "__main__":
    print(get_current_location())


#_______________pip install geocoder geopy
#_______________python test8.py