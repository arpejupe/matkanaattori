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

var userGeolocation;

function geo_success(position) {

    userGeolocation = position;

    $.ajax({
        url: "http://localhost:8080/location/",
        type: "GET",
        contentType: "text/xml; charset=utf-8",
        data: {
            "lat": position.coords.latitude,
            "lng": position.coords.longitude
        },
        success: function (data) {
            console.log(data);
            if(data["error"]) {
                $("#timer_frame").hide();
                $("#error").text("Error: " + data["error_msg"]).show();
            }
            else {
                $("#error").hide();
                var time_counter = new Date();
                time_counter.setSeconds(data["time_left"]);
                $('#countdown').countdown({until: time_counter});
                $("#next_event").text(data["next_event"]);
                $("#timer_frame").fadeIn();
            }
        },
        error: function () {
            $("#timer_frame").hide();
            $("#error").text("Error: Couldn't calculate next event!").show();
        }
    });
}

navigator.geolocation.getCurrentPosition(function (position) {
    userGeolocation = position;
    geo_success(position);
    // to watch position change
    var wpid = navigator.geolocation.watchPosition(function (position) {
        //console.log(position.coords);
        if (position.coords.latitude != userGeolocation.coords.latitude
            || position.coords.longitude != userGeolocation.coords.longitude) {
              $('#countdown').countdown("destroy");
              geo_success(position);
        }
    }, geo_error, geo_options);
}, geo_error, geo_options);
