/*
    Javascript for geolocation
    src: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/Using_geolocation
*/

function geo_success(position) {
    do_something(position.coords.latitude, position.coords.longitude);
}

function geo_error() {
    alert("Sorry, no position available.");
}

var geo_options = {
    enableHighAccuracy: true,
    maximumAge: 30000, // age of cached position is accepted in milliseconds
    //timeout: 27000 // geo_error when position retrieval times out
};


if ("geolocation" in navigator) {
    /* geolocation is available */
    // get current position, calls geo_success on success
    navigator.geolocation.getCurrentPosition(geo_success, geo_error, geo_options);
    // watch position changes, calls geo_success on success
    var wpid = navigator.geolocation.watchPosition(geo_success, geo_error, geo_options);
} else {
    /* geolocation IS NOT available */
    alert("Sorry, geolocation is not supported.");
}

function do_something(x, y) {
    console.log(x, y);
    $.ajax({
        url: "http://localhost:8080/locate",
        type: "GET",
        data: {"start": x + "," + y, "destination":"3433184,6905220" },
            contentType: "text/xml; charset=utf-8",
        success: function (data) {
            //called when successful
            console.log(data);
        },
        error: function (e) {
            //called when there is an error
            console.log(e.message);
        }
    });
}
