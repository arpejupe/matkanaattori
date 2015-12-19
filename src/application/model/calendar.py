from requests import get
from icalendar import Calendar
from datetime import datetime
import pytz
import pylibmc

cache = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

def getCalendar(url):
    request = get(url)
    if request.status_code is 200:
        return Calendar.from_ical(request.content)
    return None

def getCalendarEvents(url):
    calendar = getCalendar(url)
    events = calendar.walk("vevent")
    return parseEvents(events)

def getNextEvent(*urls):
    allevents = []
    for url in urls:
        url = str(url)
        cachedEvents = cache.get(url)
        if cachedEvents is None:
            cachedEvents = getCalendarEvents(url)
            # cache values: number of events, expire time in seconds
            cache.set(url, cachedEvents[:10], 1800)
        allevents += cachedEvents
    currentTime = getCurrentTime()
    for event in sorted(allevents, key=lambda event: event["startTime"]):
        if event["startTime"] > currentTime:
            return event
    return None

def parseEvents(events):
    currentTime = getCurrentTime()
    # parse past events and include only required data
    events = [{"summary": event.get("summary").to_ical(),
                "startTime": event.get("dtstart").dt,
                "location": str(event.get("location"))} for event in events if event.get("dtstart").dt >= currentTime]
    return sorted(events, key=lambda event: event["startTime"])

def getCurrentTime():
    return pytz.utc.localize(datetime.now())

if __name__ == '__main__':
    calendars = ["https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a"]
    nextEvent = getNextEvent(*calendars)
    print(nextEvent)
