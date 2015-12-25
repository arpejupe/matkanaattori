# -*- coding: utf-8 -*-

import cherrypy
import json
import datetime
import pytz

from library import coordinates

from application.model import calendar
from application.model.matkaroute import MatkaRoute
from application.model.jyulocation import JyuLocation

class LocationException(Exception):
    pass

class LocationModel(object):

    def calculate(self, lat=None, lng=None, userinfo=None):
        try:
            nextEvent = calendar.getNextEvent(*userinfo['calendar_url'])
            jyuLocation = JyuLocation(nextEvent.location)
            start_point = getKKJ3Point(lat, lng)
            end_point = getKKJ3Point(jyuLocation.coordinates.lat, jyuLocation.coordinates.lng)
            arrival_time = nextEvent.startTime.astimezone(pytz.timezone(userinfo['timezone']))
            # test start point:
            # start_point = "3597369,6784330"
            route = MatkaRoute(start_point, end_point, arrival_time, userinfo["walking_speed"])
            timeLeft = route.departure_time - datetime.datetime.now()
            return {'time_left': timeLeft.seconds, 'next_event': nextEvent.location}
        except Exception, e:
            raise LocationException(e.message)

def getKKJ3Point(lat, lng):
    kkj3_location = coordinates.WGS84lalo_to_KKJxy({"La": float(lat), "Lo": float(lng)})
    point = "%d,%d" % (int(kkj3_location["I"]), int(kkj3_location["P"]))
    return point
