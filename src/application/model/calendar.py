# -*- coding: utf-8 -*-

from requests import get
import datetime
import icalendar
import pytz
import pylibmc

cache_expiration = 600 # time in seconds after cached events expire
cache_size = 5 # number of events to store in cache

## For Heroku switch cache:
#servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
#user = os.environ.get('MEMCACHIER_USERNAME', '')
#pass = os.environ.get('MEMCACHIER_PASSWORD', '')

#cache = pylibmc.Client(servers, binary=True,
#                    username=user, password=pass,
cache = pylibmc.Client(["127.0.0.1"], binary=True,
                    behaviors={
                      # Faster IO
                      "tcp_nodelay": True,
                      "no_block": True,

                      # Timeout for set/get requests
                      "_poll_timeout": 2000,

                      # Use consistent hashing for failover
                      "ketama": True,

                      # Configure failover timings
                      "connect_timeout": 2000,
                      "remove_failed": 4,
                      "retry_timeout": 2,
                      "dead_timeout": 10,
                    })

class CalendarException(Exception):
    pass

class Event(object):
    def __init__(self, iCalEvent, timezone):
        self.summary = iCalEvent.get("summary").to_ical()
        self.setLocation(iCalEvent.get("location"))
        self.setTime(iCalEvent.get("dtstart").dt)
        self.setTimezone(timezone)

    def setTimezone(self, timezone):
        if self.startTime.tzinfo is None:
            self.startTime = timezone.localize(self.startTime)
        else:
            self.startTime = self.startTime.astimezone(timezone)

    def setTime(self, timeObject):
        if type(timeObject) is datetime.date:
            self.startTime = datetime.datetime.combine(timeObject, datetime.time())
        elif type(timeObject) is datetime.datetime:
            self.startTime = timeObject
        else:
            raise CalendarException("Event date parse error")

    def setLocation(self, location):
        if location is not None:
            self.location = location.split(",")[0]
        else:
            self.location = location

class Calendar(object):
    def __init__(self, urls, timezone):
        self.urls = urls
        self.timezone = timezone

    def getCalendar(self, url):
        request = get(url)
        if request.status_code is 200:
            return icalendar.Calendar.from_ical(request.content)
        else:
            raise CalendarException("Calendar request error (status code: %s)" % request.status_code)

    def getCalendarEvents(self, url):
        calendar = self.getCalendar(url)
        if calendar is None:
            raise CalendarException("Calendar parse error")
        events = calendar.walk("vevent")
        return self.parseEvents(events)

    def parseEvents(self, iCalEvents):
        currentTime = datetime.datetime.now(self.timezone)
        # ignore past events and events without location
        events = []
        for iCalEvent in iCalEvents:
            event = Event(iCalEvent, self.timezone)
            if event.location is not None and event.startTime >= currentTime:
                events.append(event)
        return sorted(events, key=lambda event: event.startTime)

    def getNextEvent(self):
        allEvents = []
        for url in self.urls:
            url = str(url)
            cachedEvents = cache.get(url)
            if cachedEvents is None:
                cachedEvents = self.getCalendarEvents(url)
                cache.set(url, cachedEvents[:cache_size], cache_expiration)
            allEvents += cachedEvents
        currentTime = datetime.datetime.now(self.timezone)
        for event in sorted(allEvents, key=lambda event: event.startTime):
            if event.startTime > currentTime:
                return event
        raise CalendarException("No events available")

if __name__ == '__main__':
    urls = ["https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a"]
    calendar = Calendar(urls, pytz.timezone("Europe/Helsinki"))
    print(calendar.getNextEvent())
