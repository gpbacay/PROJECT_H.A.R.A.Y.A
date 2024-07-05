import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import region_code_for_number
from opencage.geocoder import OpenCageGeocode
import folium


key = "05f82aa82b584f6b8d4224a4262d4d5d"

number = "+639555091630"
pepnumber = phonenumbers.parse(number=number)
location = geocoder.description_for_number(pepnumber, "en")
location1 = geocoder.country_name_for_number(pepnumber, "en")
print(location)
print(location1)

service_pro = phonenumbers.parse(number=number)
print(carrier.name_for_number(service_pro, "en"))
print(region_code_for_number(numobj=service_pro))

geocoder = OpenCageGeocode(key=key)
query = str(location)
results = geocoder.geocode(query=query)
print(results)
print("\n")

lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
print(lat, lng)

myMap = folium.Map(location=[lat, lng], zoom_start=9)
folium.Marker([lat, lng], popup=location).add_to(myMap)

myMap.show_in_browser()


#_______pip install phonenumbers
#_______pip install opencage
#_______pip install folium
#_______python test9.py
