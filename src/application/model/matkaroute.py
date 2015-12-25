# -*- coding: utf-8 -*-

from urllib import urlencode
from xml.etree import ElementTree
from requests import get
from datetime import datetime
from pytz import timezone

matka_api = "http://api.matka.fi/?"
matka_api_timezone = timezone("Europe/Helsinki")
api_user = "matkanaattori"
api_pass = "ties532soa"

class MatkaException(Exception):
    pass

class MatkaRoute(object):
    # a: start point
    # b: destination point
    # time: date and time of departure/arrival
    # timemode: time is 1: the time of departure, 2: the time of arrival
    # show: number of valid routing results
    # walkspeed: walking speeds 1,2,3,4,5
    def __init__(self, a, b, time, walkspeed, timemode="2", show="1"):
        self.start_point = a
        self.end_point = b
        self.time = time.astimezone(matka_api_timezone)
        self.walkspeed = walkspeed
        self.timemode = timemode
        self.show = show
        self.departure_time = self.getRouteDepartureTime()

    def getRoute(self):
        params = urlencode({
            "a": self.start_point,
            "b": self.end_point,
            "time": self.time.strftime("%H%M"),
            "date": self.time.strftime("%Y%m%d"),
            "timemode": self.timemode,
            "show": self.show,
            "walkspeed": self.walkspeed,
            "user": api_user,
            "pass": api_pass
        })
        request = get(matka_api + params, stream=True)
        if request.status_code is 200:
            request.raw.decode_content = True
            return ElementTree.iterparse(request.raw)
        else:
            raise MatkaException("Route not available (status code %s) with params: %s" % (request.status_code, params))

    def getRouteDepartureTime(self):
        for elem,routeData in self.getRoute():
            if routeData.tag == "ERROR":
                raise MatkaException(routeData.text)
            elif routeData.tag == "DEPARTURE":
                departure_date = routeData.attrib["date"]
                departure_time = routeData.attrib["time"]
                datetimeObject = datetime.strptime(departure_date + departure_time, "%Y%m%d%H%M")
                return matka_api_timezone.localize(datetimeObject)

if __name__ == '__main__':
    route = MatkaRoute("3597369,6784330", "3392009,6686355", datetime.now(matka_api_timezone), "2")
    print route.departure_time
