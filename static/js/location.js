// Initialize and add the map
// https://developers.google.com/maps/documentation/javascript/geolocation
let map, infoWindow;
function initMap() {
  const coords = localStorage.getItem('crds').split(",").map(Number)
  const userCoords = { lat: coords[0], lng: coords[1] };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: userCoords,
  });
  // // 장소 검색
  // const searchedPlace = document.querySelector("#pac-input")
  // const searchButton = document.querySelector("#searchButton")
  // var request = {
  //   query : "인천",
  //   fields: ['name', 'geometry'],
  // };
  
  // var service = new google.maps.places.PlacesService(map);
  // service.findPlaceFromQuery(request, function(results, status) {
  // if (status === google.maps.places.PlacesServiceStatus.OK) {
  //   map.setCenter(results[0].geometry.location);
  // }
  // });

  // 위치 정보 동기화 : 지연시간 짧도록 수정
  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
    locationButton.textContent = "+";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
    locationButton.addEventListener("click", () => {
      const pos = {
        // DB에서 위치값 가져오기
        // lat: position.coords.latitude,
        // lng: position.coords.longitude,
        lat : 37.3311,
        lng : 126.5811,
      };
      map.setCenter(pos);
      if (navigator.geolocation==false){
        handleLocationError(false, infoWindow, map.getCenter());
      }
    })
    
    function handleLocationError(browserHasGeolocation) {
      console.log(
        browserHasGeolocation
          ? "Error: The Geolocation service failed."
          : "Error: Your browser doesn't support geolocation."
      );
    }
    // 지도 클릭시 좌표 반환
    const marker = new google.maps.Marker({
      position: userCoords,
      map: map,
    });
    map.addListener("click", (mapsMouseEvent) => {
      // Create a new InfoWindow.
      const clickedCoordsJson = mapsMouseEvent.latLng.toJSON()
      const clickedCoords = {lat:parseFloat(clickedCoordsJson['lat']),lng:parseFloat(clickedCoordsJson['lng'])}
      const marker = new google.maps.Marker({
        position: clickedCoords,
        map: map,
      });
      // Input창에 위치 넣기
      const exampleInput = document.querySelector("#clicked")
      const geocoder = new google.maps.Geocoder();
      geocoder.geocode({location:clickedCoords})
      .then((response)=>exampleInput.value = response.results[0].formatted_address.split(" ").slice(3,5).join(" "))
    });
    
}
  
window.initMap = initMap;

