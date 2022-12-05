// Initialize and add the map
function initMap() {
    // The location of Uluru
    const coords = localStorage.getItem('crds').split(",").map(Number)
    // const uluru = { lat: -25.344, lng: 131.031 };
    const userCoords = { lat: coords[0], lng: coords[1] };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: userCoords,
    });
    // The marker, positioned at Uluru
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
      const showMarkerCoords = document.createElement("p")
      const markerCoords = document.querySelector("#markerCoords")
      showMarkerCoords.innerHTML = [clickedCoords['lat'], clickedCoords['lng']]
      markerCoords.appendChild(showMarkerCoords)
    });
}
  
window.initMap = initMap;
