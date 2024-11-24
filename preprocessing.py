import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

cleaned_data = pd.read_csv("cleaned_properties.csv")
cleaned_data["Address"] = cleaned_data["Address"] + ", Rochester, NY"

geolocator = Nominatim(user_agent="real_estate_analytics")

# Obtain coordinates
def get_coordinates(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        pass
    return None, None

latitudes = []
longitudes = []

# Retrieve address
for address in cleaned_data["Address"]:
    lat, lng = get_coordinates(address)
    latitudes.append(lat)
    longitudes.append(lng)
    print(latitudes, longitudes)
    time.sleep(1)

# Add coordinates
cleaned_data["Latitude"] = latitudes
cleaned_data["Longitude"] = longitudes

print(cleaned_data)

cleaned_data.to_csv("cleaned_properties_with_coordinates.csv", index=False)
