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
var userGeolocation;

function tic() {
    timeleft -= 1;
    updateTime();
}

function updateTime() {
    var hours = Math.floor(timeleft / 3600);
    var minutes = Math.floor((timeleft - (hours * 3600)) / 60);
    var seconds = timeleft - (hours * 3600) - (minutes * 60);
    $("#time_left").text(hours + "h " + minutes + "m " + seconds + "s");
}

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
                var content = $("<h2 class='error_msg'>Error: " + data["error_msg"] + "</h2>");
                $("#timer_frame").append(content);
            }
            else {
                var content = $("<div id='header_subtext'> go in <span id='time_left'></span> to next event </div>\n\
                                 <div id='header_subtext'> at <span id='next_event'>" + data["next_event"] + "</span></div>");
                $("#timer_frame").append(content);
                timeleft = data["time_left"];
                clearInterval(timer);
                timer = setInterval(tic, 1000);
                updateTime();
            }
        },
        error: function () {
            var content = $("<h2 class='error_msg'>Error: Couldn't calculate next event!</h2>");
            $("#timer_frame").append(content);
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
            geo_success(position);
        }
    }, geo_error, geo_options);
}, geo_error, geo_options);
