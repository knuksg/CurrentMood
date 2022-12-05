def recommend():
    return places


# # mac wifi주소를 가져올 수 없는 경우, web geolocation api 정확도가 더 높다.
#     # 예시 위치
#     location = requests.post(
#         f"https://www.googleapis.com/geolocation/v1/geolocate?key={gmap_api_key}",
#         json={
#             "considerIp": "true",
#             "wifiAccessPoints": [
#                 {
#                     "macAddress": "84:d4:7e:f6:99:64",
#                     "signalStrength": -54,
#                     "signalToNoiseRatio": 0,
#                 },
#                 {
#                     "macAddress": "84:d4:7e:f6:99:71",
#                     "signalStrength": -43,
#                     "signalToNoiseRatio": 0,
#                 },
#                 {
#                     "macAddress": "84:d4:7e:f7:21:35",
#                     "signalStrength": -32,
#                     "signalToNoiseRatio": 0,
#                 },
#             ],
#         },
#     ).json()
#     # coords = location["location"]
#     # user_loc = choose_location(coords["lat"], coords["lng"])["user_loc"]
#     # geocoded = choose_location(coords["lat"], coords["lng"])["geocoded"]
