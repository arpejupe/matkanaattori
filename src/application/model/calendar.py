# -*- coding: utf-8 -*-

from requests import get
from datetime import datetime
import icalendar
import pytz
import pylibmc

cache = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

class CalendarException(Exception):
    pass

class Event(object):
    def __init__(self, iCalEvent, timezone):
        self.summary = iCalEvent.get("summary").to_ical()
        self.startTime = iCalEvent.get("dtstart").dt
        self.location = str(iCalEvent.get("location"))
        self.setTimezone(timezone)

    def setTimezone(self, timezone):
        if self.startTime.tzinfo is None:
            self.startTime = timezone.localize(self.startTime)
        else:
            self.startTime = self.startTime.astimezone(timezone)

class Calendar(object):
    def __init__(self, urls, timezone):
        self.urls = urls
        self.timezone = timezone

    def getCalendar(self, url):
        request = get(url)
        if request.status_code is 200:
            return icalendar.Calendar.from_ical(request.content)
        else:
            raise CalendarException("iCal url returned status code: %s" % request.status_code)

    def getCalendarEvents(self, url):
        calendar = getCalendar(url)
        events = calendar.walk("vevent")
        return parseEvents(events)

    def parseEvents(self, iCalEvents):
        currentTime = datetime.now(self.timezone)
        # parse past events and include only required data
        events = [Event(event_data, self.timezone) for event_data in iCalEvents
            if event_data.get("dtstart").dt >= currentTime]
        return sorted(events, key=lambda event: event.startTime)

    def getNextEvent(self):
        allEvents = []
        for url in self.urls:
            url = str(url)
            cachedEvents = cache.get(url)
            if cachedEvents is None:
                cachedEvents = getCalendarEvents(url)
                # cache values: number of events, expire time in seconds
                cache.set(url, cachedEvents[:10], 1800)
            allEvents += cachedEvents
        currentTime = datetime.now(self.timezone)
        for event in sorted(allEvents, key=lambda event: event.startTime):
            if event.startTime > currentTime:
                return event
        raise CalendarException("Next event not available")

if __name__ == '__main__':
    urls = ["https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a"]
    calendar = Calendar(urls, pytz.timezone("Europe/Helsinki"))
    print(calendar.getNextEvent())
