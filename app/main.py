import cherrypy
import requests
import os
import template
import auth

from cgi import escape

#for debugging
from pprint import pprint

DB_STRING = "matkanaattori.db"
SESSION_KEY = '_cp_username'

class MatkaClient(object):
    
    main = template.MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', main)

    @cherrypy.tools.mako(filename="index.html")
    @cherrypy.expose
    def index(self):
        return {"user" : cherrypy.session.get(SESSION_KEY)}
    
    @cherrypy.tools.mako(filename="login.html")
    @cherrypy.expose
    def login(self, username=None, password=None):
        #username = escape(username) does not work, need proper validation
        #password = escape(password)
        if username is None or password is None:
            return {'username': username,
                    'msg': 'Please login by giving username and password:'}
        
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
        '/locate': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/xml')],
        },
        '/service': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/register': {
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