import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

load_dotenv()

opencage_api_key = os.getenv("OPENCAGE_API_KEY")


def get_geo_info(location):
    geocoder = OpenCageGeocode(opencage_api_key)

    result = geocoder.geocode(location)

    if result:
        latitude = result[0]["geometry"]["lat"]
        longitude = result[0]["geometry"]["lng"]
    else:
        print("Location not found.")

    return latitude, longitude
