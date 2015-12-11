/*
    Javascript for geolocation
    src: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/Using_geolocation
*/

function geo_error() {
    console.log("no position available");
}
var geo_options = {
    enableHighAccuracy: true,
    maximumAge: 30000, // age of cached position is accepted in milliseconds
    //timeout: 27000 // geo_error when position retrieval times out
};

var timeleft = 0;
var timer;

function tic() {
    timeleft -= 1;
    var minutes = Math.floor(timeleft / 60);
    seconds = timeleft - minutes * 60;
    document.getElementById("timeleft").innerHTML = minutes + ":" + seconds;
}

navigator.geolocation.getCurrentPosition(function(position) {
    $.ajax({
        url: "http://localhost:8080/locate/${user}",
        type: "GET",
        data: {"lat":position.coords.latitude,
               "lng":position.coords.longitude },
        contentType: "text/xml; charset=utf-8",
        success: function (data) {
            console.log(data);
            timeleft = data["result"];
            timer = setInterval(tic, 1000);
        },
        error: function (e) {
            console.log(e.message);
        }
    });
}, geo_error, geo_options);
// to watch position change
// var wpid = navigator.geolocation.watchPosition(geo_success, geo_error, geo_options);