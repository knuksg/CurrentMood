// Initialize and add the map
// https://developers.google.com/maps/documentation/javascript/geolocation
// 지도생성
let map, infoWindow;

function initMap() {
  const coords = localStorage.getItem('crds').split(",").map(Number)
  const userCoords = { lat: coords[0], lng: coords[1] };
  // const currentLocationCoords = currentLocation.split(",")
  // const userCoords = {lat:Number(currentLocationCoords[0]), lng:Number(currentLocationCoords[1])}
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 20,
    center: userCoords,
    gestureHandling: "none", // 지도 이동 금지
    zoomControl:false, // 확대/축소 금지
  });
  // map.setOptions({draggable:false}); // 지도 이동 금지
  
  // // 장소 검색
  // https://velog.io/@gkwlsdl1/Django-redis-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0

  // 위치 정보 동기화 : 지연시간 짧도록 수정
  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
    locationButton.textContent = "+";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
    locationButton.addEventListener("click", () => {
      const pos = {
        // DB/server에서 위치값 가져오기
        // lat: position.coords.latitude,
        // lng: position.coords.longitude,
        lat : coords[0],
        lng : coords[1],
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
      // const marker = new google.maps.Marker({
        //   position: clickedCoords,
        //   map: map,
        // });
      // Input창에 위치 넣기
      const exampleInput = document.querySelector("#clicked")
      const clickedPlace = map.__gm.eventCapturer.innerText.split("\n")[0]
      localStorage.setItem("clickedPlace",clickedPlace) // 1
      console.log(map.__gm.eventCapturer.innerText.split("\n")[0])
      exampleInput.value = map.__gm.eventCapturer.innerText.split("\n")[0]
      const geocoder = new google.maps.Geocoder();
      const clickedCoordsJson = mapsMouseEvent.latLng.toJSON()
      const clickedCoords = {lat:parseFloat(clickedCoordsJson['lat']),lng:parseFloat(clickedCoordsJson['lng'])}
      // 좌표 geocoding => 주소
      // geocoder.geocode({location:clickedCoords})
      // .then(function(response){
      //   // exampleInput.value = response.results[0].formatted_address.split(" ").slice(3,5).join(" ")
      //   // 텍스트 검색
      //   var request = {
      //     location: map.getCenter(),
      //     radius: '500',
      //     query: response.results[0].formatted_address
      //   };
      
      //   var service = new google.maps.places.PlacesService(map);
      //   service.textSearch(request, callback);
      //   function callback(results){
      //     console.log(results[0])
      //   }
      // })
      // console.log(currentLocation.split(",")[0])
    });
    // 검색바
    const mapsearch = document.getElementById("mapsearch")
    var searchBox = new google.maps.places.SearchBox(mapsearch)
    // 검색위치
    google.maps.event.addListener(searchBox,'places_changed',function(){
      var places = searchBox.getPlaces();
      var bounds = new google.maps.LatLngBounds();
      var i, place;
      for (i=0; place=places[i];i++){
        // console.log(place.geometry.location);
        bounds.extend(place.geometry.location);
        marker.setPosition(place.geometry.location)
      }
      map.fitBounds(bounds);
      map.setZoom(17)
    })
}
  
window.initMap = initMap;


