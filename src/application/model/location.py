# -*- coding: utf-8 -*-

import cherrypy
import json
import datetime
import pytz

from library import coordinates

from application.model import calendar
from application.model import matkaprovider
from application.model import jyulocation

class LocationException(Exception):
    pass

class LocationModel(object):

    def calculate(self, lat=None, lng=None, userinfo=None):
        try:
            nextEvent = calendar.getNextEvent(*userinfo['calendar_url'])
            event_location = jyulocation.getJyuLocation(nextEvent.location)
            kkj3_event_location = coordinates.WGS84lalo_to_KKJxy({"La": event_location.lat,
                                                                  "Lo": event_location.lng})
            kkj3_user_location = coordinates.WGS84lalo_to_KKJxy({"La": float(lat),
                                                               "Lo": float(lng)})
            start_point = "%d,%d" % (int(kkj3_user_location["I"]), int(kkj3_user_location["P"]))
            end_point = "%d,%d" % (int(kkj3_event_location["I"]), int(kkj3_event_location["P"]))
            arrival_time = nextEvent.startTime.astimezone(pytz.timezone(userinfo['timezone']))
            departure_time = matkaprovider.getRouteDepartureTime(start_point, end_point, arrival_time, userinfo["walking_speed"])
            timeLeft = departure_time - datetime.datetime.now()
            return {'time_left': timeLeft.seconds, 'next_event': nextEvent.location}
        except Exception, e:
            raise LocationException(e.message)
