// csrf 가져오기
var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // web geolocation으로 좌표값 가져오기
  var options = {
    enableHighAccuracy: false,
    timeout: 10000,
    maximumAge: 0
  };
  
  function success(pos) {
    var usrCrd = [37.25233,127.48984] // 임시좌표
    // console.log([usrCrd[0],usrCrd[1]])
    var crd = pos.coords;
    // const usrCrd = [crd.latitude,crd.longitude]
    localStorage.setItem('crds',usrCrd)
    // const request = new XMLHttpRequest;
    // request.open('POST','http://127.0.0.1:8000/locations/')
    // request.setRequestHeader("X-CSRFToken", csrftoken); 
    // request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    // request.send(`userLocation=${usrCrd}`)
    // request.onreadystatechange=function(event){
    // console.log('location send')
    // }
  }
  
  function error(err) {
    console.warn(`ERROR(${err.code}): ${err.message}`);
  }
  // 위치 DB 지속적으로 보내주기
// navigator.geolocation.watchPosition(success,error,options)