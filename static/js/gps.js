// csrftoken 생성
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
  var csrftoken = getCookie('csrftoken');
  
  
  
  // web geolocation으로 좌표값 가져오기
  var options = {
    enableHighAccuracy: false,
    timeout: 10000,
    maximumAge: 0
  };
  
  function success(pos) {
    var usrCrd = [37.55483,126.95498] // 임시좌표
    console.log([usrCrd[0],usrCrd[1]])
    var crd = pos.coords;
    // const usrCrd = [crd.latitude,crd.longitude]
    // result.innerHTML= [crd.latitude,crd.longitude]
    // 1. form으로 전송하기
    // const reqForm = document.querySelector("#locationForm")
    // reqForm.userLocation.value = usrCrd
    // 2. 다른 방법
    localStorage.setItem('crds',usrCrd)
    const request = new XMLHttpRequest;
    request.open('POST',`http://127.0.0.1:8000/locations/`)
    request.setRequestHeader("X-CSRFToken", csrftoken); 
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.send(`userLocation=${usrCrd}`)
    request.onreadystatechange=function(event){
    console.log('location send')
  }
  }
  
  function error(err) {
    console.warn(`ERROR(${err.code}): ${err.message}`);
  }
  // 위치 DB 지속적으로 보내주기
  navigator.geolocation.watchPosition(success,error,options)