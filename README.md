Matkanaattori
========

## Documentation of choices

### Environment and tooling
Build with Python and CherryPy web framework.

Deployed using Amazon AWS virtual machine.

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

## How to setup
Install python 2.7, python-virtualenv and other required dependencies.
With apt:
    $ apt-get install python python-virtualenv libmemcached-dev libsnappy-dev zlib1g-dev
Create new virtualenv and activate it:
    $ virtualenv venv
    $ source venv/bin/activate
Install required python libraries with pip:
    $ pip install -r requirements.txt
Start with main.py:
    $ python main.py

## Python library dependencies
All external python library dependencies are listed in the requirements.txt file.

## jQuery plugins
For time countdown we use Countdown jQuery plugin written by Keith Wood.

## Team
Arttu Pekkarinen
Juha Moisio
