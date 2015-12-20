# -*- coding: utf-8 -*-
import cgi
import cherrypy

from application.model.register import RegisterModel, SubmitException
from library.format import xstr
from config import constant

class RegisterController(object):
    
    def __init__(self):
        self.register = RegisterModel()
        
    @cherrypy.tools.mako(filename="register.html")
    @cherrypy.expose
    def index(self, username=None, password=None, timezone=None, calendar_url=None):
        if username is None or password is None or timezone is None or calendar_url is None:
            return {'register': False,
                    'pointer': "Register",
                    'msg': 'Please register by providing the following information.',
                    'username': xstr(username),
                    'password': xstr(password),
                    'calendar_url': xstr(calendar_url)}
                    
    @cherrypy.tools.mako(filename="register.html")
    @cherrypy.expose
    def submit(self, username=None, password=None, timezone=None, calendar_url=None):
        try:
            self.register.submit(username, password, timezone, calendar_url)
            return {'register': True,
                    'pointer': "Register",
                    'msg': 'Regisration successful! You can now login.'} 
        except SubmitException as ex:
            return {'register': False,
                    'pointer': "Register",
                    'error_msg': ex.message,
                    'username': username,
                    'password': password,
                    'calendar_url': calendar_url}  