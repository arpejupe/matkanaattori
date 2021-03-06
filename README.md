Matkanaattori
============

App which helps people to be in time. Matkanaattori displays how much time the
user has left before he has to leave to make it to the next event. By combining
info from user provided calendar, matka.fi API, jyulocation (a tool for
converting University classrooms to locations) and browsers GeoLocation
javascript API application is able to calculate the ETA when user needs to leave.

How it works:
- User provides his timezone information and a URL for his calendar information
(i.e google calendar).
- The user can specify what his walking/cycling speed is.
    slow:30m/min)
    normal (70m/min)
    fast (100m/min)
    running (200m/min)
    cycling (300m/min)
- User navigates to calculate view showing how much time he has left before he
should leave to make it to the next event in his calendar. The page also shows
information about the first stage of the journey. This beginning of the journey
is based on the location of the user as provided by the browser and the current
time. The end of the journey is based on the location information attached to
the next event and its start time.
- In addition user can install the application as browser plugin which will
notify when user needs to leave


## Team
Arttu Pekkarinen & Juha Moisio

## Documentation of choices

### Environment and tooling
Built with Python
Database sqllite3
Deployed using Amazon AWS virtual machine.

### Architecture and project layout
Application is made by using CherryPy framework and it follows MVC pattern and
project layout represented by Sylvain Hellegouarch in Twiseless:
https://bitbucket.org/Lawouach/twiseless/src/d171fde9e454b97d519fef30af48b5c70ff08fbc?at=default

Directory Layout:

 * main.py: The bootstrap which handles the launching, setups, loading of all modules and
   controllers, and defining constants. Please note that you setup and clean database from here
   by commenting and uncommenting!
 * application: Matkanator applications divided in models, views and controllers. For viewing
   template engine called Mako is used.
 * config: CherryPy config files and constants
 * library: all the external libraries used to handle resources and help in operations
 * log: access and error log files
 * static: static files such as Javascript, CSS, etc.

### Used resources
- Matka API for public travel routing
- GeoConversion (coordinates.py)
- jyulocation service
- GeoLocation from browser
- user provided info: iCal calendar, timezone and settings

### Caching of calendars
Using memcached we cache 5 most recent upcoming calendar events with expiration
time of 10 minutes.

### Caching strategy for jyulocation service
For the caching of Jyu locations we decided for the caching strategy to use
LRU (least recently used) caching algorithm with maximum size limit.
Location data provided by the service is constant and static data that don't
expire. LRU favors the popular locations among the users' calendar events.

### Time source and timezones
We use server time and user provided timezone for calendar events. For Matka API
time is converted to be in Europe/Helsinki timezone.

Python datetime objects take timezones into account in time comparison. If the
icalendar parser cannot parse a timezone for calendar event then we use the user
provided timezone.

### Browser extension
The browser extension is created for Firefox using the Firefox Add-on SDK.

Firefox Add-on SDK includes jpm command line developer tool. Follow the
installation instructions to install the jpm tool:
https://developer.mozilla.org/en-US/Add-ons/SDK/Tools/jpm#Installation

To run the extension with jpm:
    ```
    cd matkanaattori/extension
    jpm run
    ```
To package the extension:
    ```
    jpm xpi
    ```
And run with Firefox Developer Edition with xpinstall.signatures.required disable
in about:config. With jpm the extension can be signed for distribution
(API keys required):
```
jpm sign --api-key ${AMO_API_KEY} --api-secret ${AMO_API_SECRET}
```

## How to setup

1) Install python 2.7, python-virtualenv, memcached and other required dependencies.
2) Install required dependencies with apt:
    ```
    apt-get install python python-virtualenv memcached libmemcached-dev libsnappy-dev zlib1g-dev
    ```
3) Create new virtualenv and activate it:
    ```
    virtualenv venv
    source venv/bin/activate
    ```
4) Install required python libraries with pip:
    ```
    pip install -r requirements.txt
    ```
5) Start local memcached in background:
    ```
    memcached 127.0.0.1
    ```
6) Start main.py in background:
   ```
   nohup python main.py
   ```

## Python library dependencies
All external python library dependencies are listed in the requirements.txt file.

## jQuery plugins
For time countdown we use Countdown jQuery plugin written by Keith Wood.

## License
Copyright (c) 2015. All rights reserved.