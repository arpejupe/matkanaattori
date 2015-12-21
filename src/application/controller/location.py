# -*- coding: utf-8 -*-

import cherrypy
import json

from application.model.location import LocationModel, LocationException
from application.model.login import require

from config import constant
   
class LocationController(object):

    def __init__(self):
        self.location = LocationModel()

    @require()
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, lat=None, lng=None):
        userinfo = cherrypy.session.get(constant.SESSION_KEY)
        if userinfo is None:
            return "Session is not set"
        try:
            return self.location.calculate(lat, lng, userinfo)
        except Exception as ex:
            cherrypy.log(ex.message, traceback=True)
            return {'error': True,
                    'pointer': "Location",
                    'error_msg': "Couldn't calculate next event!"}  

