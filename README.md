Matkanaattori
============

## Team
Arttu Pekkarinen & Juha Moisio

## License

Copyright (c) 2015
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

     * Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
     * Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.
     * Neither the name of Arttu Pekkarinen or Juha Moisio, nor the names of his
       contributors may be used to endorse or promote products derived from this
       software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
    cd matkanaattori/extension
    jpm run
To package the extension:
    jpm xpi

## How to setup
Install python 2.7, python-virtualenv, memcached and other required dependencies.
Install required dependencies with apt:
    $ apt-get install python python-virtualenv memcached libmemcached-dev libsnappy-dev zlib1g-dev
Create new virtualenv and activate it:
    $ virtualenv venv
    $ source venv/bin/activate
Install required python libraries with pip:
    $ pip install -r requirements.txt
Start local memcached in background:
    $  memcached 127.0.0.1 &
Start main.py in background:
    $ nohup python main.py &

## Python library dependencies
All external python library dependencies are listed in the requirements.txt file.

## jQuery plugins
For time countdown we use Countdown jQuery plugin written by Keith Wood.
