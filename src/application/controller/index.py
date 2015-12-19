# -*- coding: utf-8 -*-

import cgi
import cherrypy
from config import constant

__all__ = ['IndexController']

class IndexController(object):
    def __init__(self, controllers):
    	for key, value in controllers.items():
    		setattr(self, key, value)
        
    @cherrypy.expose
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        user_info = cherrypy.session.get(constant.SESSION_KEY)
        if user_info is not None:
            username = user_info['username']
        else:
            username = None
        return {"pointer": "index",
                "user" : username}