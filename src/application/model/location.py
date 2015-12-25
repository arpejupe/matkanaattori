# -*- coding: utf-8 -*-

import cherrypy
import json
import datetime
import pytz

from library import coordinates

from application.model.calendar import Calendar
from application.model.matkaroute import MatkaRoute
from application.model.jyulocation import JyuLocation

class LocationException(Exception):
    pass

class LocationModel(object):

    def calculate(self, lat=None, lng=None, userinfo=None):
        calendar = Calendar(userinfo['calendar_url'], pytz.timezone(userinfo["timezone"]))
        nextEvent = calendar.getNextEvent()
        jyuLocation = JyuLocation(nextEvent.location)
        start_point = getKKJ3Point(lat, lng)
        end_point = getKKJ3Point(jyuLocation.coordinates.lat, jyuLocation.coordinates.lng)
        arrival_time = nextEvent.startTime
        # test start point:
        # start_point = "3597369,6784330"
        route = MatkaRoute(start_point, end_point, arrival_time, userinfo["walking_speed"])
        return {
            'time_left': getTimeLeft(route.departure_time),
            'next_event': nextEvent.location}

def getKKJ3Point(lat, lng):
    kkj3_location = coordinates.WGS84lalo_to_KKJxy({"La": float(lat), "Lo": float(lng)})
    point = "%d,%d" % (int(kkj3_location["I"]), int(kkj3_location["P"]))
    return point

def getTimeLeft(end_time):
    timeLeft = end_time - datetime.datetime.now(pytz.utc)
    return int(timeLeft.total_seconds())
