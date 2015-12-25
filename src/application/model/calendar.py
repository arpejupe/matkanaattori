# -*- coding: utf-8 -*-

from requests import get
from icalendar import Calendar
from datetime import datetime
import pytz
import pylibmc

cache = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

class CalendarException(Exception):
    pass

class Event(object):
    def __init__(self, iCalEvent):
        self.summary = iCalEvent.get("summary").to_ical()
        self.startTime = iCalEvent.get("dtstart").dt
        self.location = str(iCalEvent.get("location"))

def getCalendar(url):
    request = get(url)
    if request.status_code is 200:
        return Calendar.from_ical(request.content)
    else:
        raise CalendarException("iCal url returned status code: %s" % request.status_code)

def getCalendarEvents(url):
    calendar = getCalendar(url)
    events = calendar.walk("vevent")
    return parseEvents(events)

def getNextEvent(*urls):
    allEvents = []
    for url in urls:
        url = str(url)
        cachedEvents = cache.get(url)
        if cachedEvents is None:
            cachedEvents = getCalendarEvents(url)
            # cache values: number of events, expire time in seconds
            cache.set(url, cachedEvents[:10], 1800)
        allEvents += cachedEvents
    currentTime = getCurrentTime()
    for event in sorted(allEvents, key=lambda event: event.startTime):
        if event.startTime > currentTime:
            return event
    raise CalendarException("Next event not available")

def parseEvents(iCalEvents):
    currentTime = getCurrentTime()
    # parse past events and include only required data
    events = [Event(event_data) for event_data in iCalEvents if event_data.get("dtstart").dt >= currentTime]
    return sorted(events, key=lambda event: event.startTime)

def getCurrentTime():
    return datetime.now(pytz.utc)

if __name__ == '__main__':
    calendars = ["https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a"]
    nextEvent = getNextEvent(*calendars)
    print(nextEvent)
