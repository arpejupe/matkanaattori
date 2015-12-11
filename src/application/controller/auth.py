# -*- coding: utf-8 -*-
import cgi
import cherrypy

from application.model.login import LoginModel
from library.format import xstr

from config import constant
   
class LoginController(object):
    
    def __init__(self):
        self.login = LoginModel()
        
    @cherrypy.tools.mako(filename="login.html")
    @cherrypy.expose
    def index(self, username=None, password=None):
        return {'msg': 'Please login by giving username and password:',
                'username': xstr(username)}
                    
    @cherrypy.tools.mako(filename="login.html")
    @cherrypy.expose    
    def submit(self, username=None, password=None):
        error_msg = self.login.check_credentials(username, password)
        if error_msg:
            return {'msg': error_msg,
                    'username': username}
        else:
            cherrypy.session.regenerate()
            cherrypy.session[constant.SESSION_KEY] = cherrypy.request.login = username
            raise cherrypy.HTTPRedirect("/")

class LogoutController(object):

    @cherrypy.expose
    def index(self):
        sess = cherrypy.session
        username = sess.get(constant.SESSION_KEY, None)
        sess[constant.SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
        raise cherrypy.HTTPRedirect("/")
    