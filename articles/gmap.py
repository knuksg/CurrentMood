import googlemaps
from datetime import datetime
import os

# 좌표값 -> 주소값
def reverse_geocoding(lat, lng):
    gmaps = googlemaps.Client(key=os.getenv("gmap_api"))
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng), language="ko")
    return reverse_geocode_result


# 주소 반환 값 parsing
def parsing_geocoded(lat, lng):
    geocoded = reverse_geocoding(lat, lng)
    loc = []
    for i in range(len(geocoded)):
        geocoded_locations = geocoded[i]  # 장소 객체들
        for j, k in geocoded_locations.items():
            if j == "formatted_address":
                # print("".join(k.split(",")[0:2]))
                loc.append(k)
    return {
        "loc": loc[0],
        "geocoded": geocoded,
    }
