from requests import get
from icalendar import Calendar
from datetime import datetime
import pytz

class UCalendar(Calendar):
    def __init__(self, icalurl):
        r = get(icalurl, stream=True)
        self.cal = Calendar.from_ical(r.content)

    def getNextEvent(self):
        now = datetime.now(pytz.utc)
        iterEvents = iter(self.cal.walk('vevent'))
        nextEvent = next(iterEvents)
        for event in iterEvents:
            start = event.get("dtstart").dt
            if start > now and start < nextEvent.get("dtstart").dt:
                nextEvent = event
        return nextEvent

if __name__ == '__main__':
    url = "https://korppi.jyu.fi/calendar/ical/9e861b35b1d2cdb82d8feb805e64fd43decf4dfc0b3d5d1fc177114e634ede2a"
    cal = UCalendar(url)
    nextEvent = cal.getNextEvent()
    print(nextEvent.get("summary"))
    print(nextEvent.get("location"))
    print(nextEvent.get("dtstart").dt)
