# -*- coding: utf-8 -*-
import cgi
import cherrypy

from application.model.settings import SettingsModel, SubmitException
from application.model.login import require
from library.format import xstr
from config import constant

class SettingsController(object):
    
    def __init__(self):
        self.settings = SettingsModel()
    
    @require()
    @cherrypy.expose
    @cherrypy.tools.mako(filename="settings.html")
    def index(self, timezone=None, walking_speed=None, calendar_url=None):
        userinfo = cherrypy.session.get(constant.SESSION_KEY)
        if userinfo is None:
            return "Session is not set"
        if timezone is None or walking_speed is None or calendar_url is None:
            return {'settings': False,
                    'pointer': "Settings",
                    'msg': 'You can change Matkanaattori settings.',
                    'timezone': userinfo['timezone'],
                    'walking_speed': userinfo['walking_speed'],
                    'calendar_url': userinfo['calendar_url']}
                    
    @require()
    @cherrypy.expose
    @cherrypy.tools.mako(filename="settings.html")
    def submit(self, timezone=None, walking_speed=None, calendar_url=None):
        # If calendar_url is not list, convert then
        if isinstance(calendar_url, basestring):
            calendar_url = [calendar_url]
        userinfo = cherrypy.session.get(constant.SESSION_KEY)
        if userinfo is None:
            return "Session is not set"
        try:
            self.settings.submit(userinfo['user_id'], timezone, walking_speed, calendar_url)
            raise cherrypy.HTTPRedirect("/")
        except SubmitException as ex:
            return {'settings': False,
                    'pointer': "Settings",
                    'error_msg': ex.message,
                    'timezone': timezone,
                    'walking_speed': walking_speed,
                    'calendar_url': calendar_url} 