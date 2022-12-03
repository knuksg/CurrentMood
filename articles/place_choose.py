from .gmap import geocoding

# 유저가 입력시 선택할 수 있는 주소 목록
def choose_location(lat, lng):
    geocoded = geocoding(lat, lng)
    user_loc = []
    for i in range(len(geocoded)):
        geocoded_locations = geocoded[i]  # 장소 객체들
        for j, k in geocoded_locations.items():
            if j == "formatted_address":
                # print("".join(k.split(",")[0:2]))
                user_loc.append("".join(k.split(",")[0:2]))
    print(user_loc)
    return {
        "user_loc": user_loc,
        "geocoded": geocoded,
    }
