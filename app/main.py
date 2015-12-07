DB_STRING = "matkanaattori.db"
SESSION_KEY = '_cp_username'

import cherrypy
import requests
import os
import template
import auth
import registration

import sqlite3

from cgi import escape

#for debugging
from pprint import pprint

class MatkaClient(object):
    
    template = template.MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', template)

    @cherrypy.tools.mako(filename="index.html")
    @cherrypy.expose
    def index(self):
        return {"user" : cherrypy.session.get(SESSION_KEY)}
    
    @cherrypy.tools.mako(filename="login.html")
    @cherrypy.expose
    def login(self, username=None, password=None):
        #username = escape(username) does not work, need proper validation
        #password = escape(password)
        with sqlite3.connect(DB_STRING) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM user")
            list = cur.fetchall();
        if username is None or password is None:
            return {'username': username,
                    'msg': 'Please login by giving username and password:',
                    'list': list}
        
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
                    'username': username,
                    'msg': 'Please register by providing username, password, timezone and calendar url'}
                    
        register = registration.submit(username, password, timezone, calendar_url)
        if register is False:
            return {'register': register,
                    'msg': 'Registeration failed, please try again',
                    'username': username,
                    'password': password,
                    'timezone': timezone,
                    'calendar_url': calendar_url}     
        else:
            return {'register': register,
                    'msg': 'Regisration successful!'}  
        
    @cherrypy.expose
    @auth.require()
    def locate(self, start, destination):
        # Kortepohja x="3433184" y="6905220"
        # http://api.matka.fi/?a=3597369,6784330&b=3433184,6905220&user=matkanaattori&pass=ties532soa
        response = requests.get("http://api.matka.fi/?a=" + start + "&b=" + destination + "&user=matkanaattori&pass=ties532soa")
        xml = response.text
        return xml
    
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
            'tools.response_headers.headers': [('Content-Type', 'text/xml')],
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

if __name__ == '__main__':
    cherrypy.quickstart(Root())