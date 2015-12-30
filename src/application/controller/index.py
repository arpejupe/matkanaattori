# -*- coding: utf-8 -*-

import os
import cgi
import cherrypy
from config import constant
from cherrypy.lib.static import serve_file

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

    @cherrypy.expose
    def extension(self):
        downloadPath = '/home/ubuntu/extension/matkanaattori_addon-1.0.0-fx+an.xpi'
        filepath = os.path.abspath(downloadPath)
        return serve_file(filepath, "application/x-download", "attachment")
