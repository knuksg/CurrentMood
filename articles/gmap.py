import googlemaps
from datetime import datetime
import os


def geocoding(lat, lng):
    gmaps = googlemaps.Client(key=os.getenv("gmap_api"))
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    return reverse_geocode_result


def geolocation():
    return none
