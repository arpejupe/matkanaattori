from requests import get
from icalendar import Calendar
from datetime import datetime
import pytz
import pylibmc

cache = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

class Events(object):
    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    def getNextEvent(self):
        iterEvents = iter(self.events)
        nextEvent = next(iterEvents)
        now = datetime.now(nextEvent["start"].tzinfo)
        for event in iterEvents:
            start = event["start"]
            if start > now and start < nextEvent["start"]:
                nextEvent = event
        return nextEvent

    def join(self, eventsObj):
        self.events += eventsObj.events

def getiCalEvents(url):
    url = str(url)
    events = cache.get(url)
    if events is None:
        events = Events()
        present = datetime.now(pytz.utc)
        r = get(url, stream=True)
        calendar = Calendar.from_ical(r.content)
        for event in calendar.walk('vevent'):
            start = event.get("dtstart").dt
            location = event.get("location")
            if start > present:
                events.addEvent({"start": start,
                                 "location": str(location)})
        cache.set(url, events, time=1800)
    return events

def getEventsForAll(urls):
    events = Events()
    for url in urls:
        events.join(getiCalEvents(url))
    return events

if __name__ == '__main__':
    calendars = ["https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a",
            "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a"]
    for x in range(0,5):
        events = getEventsForAll(calendars)
        nextEvent = events.getNextEvent()
        print(nextEvent)
