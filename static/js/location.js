// Initialize and add the map
// https://developers.google.com/maps/documentation/javascript/geolocation
let map, infoWindow;
function initMap() {
    const coords = localStorage.getItem('crds').split(",").map(Number)
    const userCoords = { lat: coords[0], lng: coords[1] };
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: userCoords,
    });
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
      infoWindow.setPosition(pos);
      infoWindow.setContent("현재위치");
      infoWindow.open(map);
      map.setCenter(pos);
      if (navigator.geolocation==false){
        handleLocationError(false, infoWindow, map.getCenter());
      }
    })
    
    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
      infoWindow.setPosition(pos);
      infoWindow.setContent(
        browserHasGeolocation
          ? "Error: The Geolocation service failed."
          : "Error: Your browser doesn't support geolocation."
      );
      infoWindow.open(map);
    }
    // 지도 클릭시 좌표 반환
    const marker = new google.maps.Marker({
      position: userCoords,
      map: map,
    });
    map.addListener("click", (mapsMouseEvent) => {
      // Create a new InfoWindow.
      const clickedCoordsJson = mapsMouseEvent.latLng.toJSON()
      const clickedCoords = {lat:Number(clickedCoordsJson['lat']),lng:Number(clickedCoordsJson['lng'])}
      const marker = new google.maps.Marker({
        position: clickedCoords,
        map: map,
      });
      const markerCoords = [clickedCoords['lat'], clickedCoords['lng']]
      // Input창에 위치 넣기
      const exampleInput = document.querySelector("#exampleInput")
      exampleInput.value = markerCoords
    });
    
}
  
window.initMap = initMap;

