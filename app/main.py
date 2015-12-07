DB_STRING = "matkanaattori.db"
SESSION_KEY = '_cp_username'

import cherrypy
import requests
import os
import sys
import template
import auth
import registration
import sqlite3

from lib import calendarprovider

from registration import SubmitException

#for debugging
from pprint import pprint

def xstr(s):
    return '' if s is None else str(s)

class MatkaClient(object):
    
    template = template.MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', template)

    @cherrypy.tools.mako(filename="index.html")
    @cherrypy.expose
    def index(self):
        #Tahan kaikki informaatiosala toistaiseksi
        return {"user" : cherrypy.session.get(SESSION_KEY)}
    
    @cherrypy.tools.mako(filename="login.html")
    @cherrypy.expose
    def login(self, username=None, password=None):
        if username is None or password is None:
            return {'msg': 'Please login by giving username and password:',
                    'username': xstr(username)}
        
        error_msg = auth.check_credentials(username, password)
        if error_msg:
            return {'username': username,
                    'msg': error_msg}
        else:
            cherrypy.session.regenerate()
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            raise cherrypy.HTTPRedirect("/")
        
    @cherrypy.expose
    def logout(self):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
        raise cherrypy.HTTPRedirect("/")
    
    @cherrypy.tools.mako(filename="register.html")
    @cherrypy.expose
    def register(self, username=None, password=None, timezone=None, calendar_url=None):
        if username is None or password is None or timezone is None or calendar_url is None:
            return {'register': False,
                    'msg': 'Please register by providing username, password, timezone and calendar url',
                    'username': xstr(username),
                    'password': xstr(password),
                    'timezone': xstr(timezone),
                    'calendar_url': xstr(calendar_url)}
        try:
            registration.submit(username, password, timezone, calendar_url)
            return {'register': True,
                    'msg': 'Regisration successful!'} 
        except SubmitException as ex:
            return {'register': False,
                    'msg': ex.message,
                    'username': username,
                    'password': password,
                    'timezone': timezone,
                    'calendar_url': calendar_url}  
        
    @cherrypy.tools.mako(filename="locate.html")
    @cherrypy.expose
    def locate(self, username):
        # Kortepohja x="3433184" y="6905220"
        # http://api.matka.fi/?a=3597369,6784330&b=3433184,6905220&user=matkanaattori&pass=ties532soa
        #response = requests.get("http://api.matka.fi/?a=" + start + "&b=" + destination + "&user=matkanaattori&pass=ties532soa")
        #xml = response.text
        #return xml
        with sqlite3.connect(DB_STRING) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM user WHERE username=:username", 
                        {'username': username})
            result = cur.fetchone()
            calendar_url = result[3]
            
            events = calendarprovider.getiCalEvents(calendar_url);
            return {'result': events.getNextEvent()} 
    
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.mako.collection_size': 500,
            'tools.mako.directories': 'views/',
            'tools.sessions.on': True,
            'tools.auth.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/login': {
            'tools.mako.collection_size': 500,
            'tools.mako.directories': 'views/',
            'tools.sessions.on': True,
            'tools.auth.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/register': {
            'tools.mako.collection_size': 500,
            'tools.mako.directories': 'views/',
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/locate': {
            'tools.response_headers.on': True,
            'tools.sessions.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/service': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './resources'
        }
    }
    
    webapp = MatkaClient()
    cherrypy.quickstart(webapp, '/', conf)