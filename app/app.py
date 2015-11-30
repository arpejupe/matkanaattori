import cherrypy
import requests
import os, os.path
import sqlite3
import time
 
#for debugging
from pprint import pprint

DB_STRING = "matkanaattori.db"

class MatkaClient(object):
    @cherrypy.expose
    def index(self):
        return open('views/index.html')

    @cherrypy.expose
    def locate(self, start, destination):
        # http://api.matka.fi/?a=3597369,6784330&b=3392009,6686355&user=matkanaattori&pass=ties532soa
        response = requests.get("http://api.matka.fi/?a=" + start + "&b=" + destination + "&user=matkanaattori&pass=ties532soa")
        xml = response.text
        return xml


class MatkaService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']
    
    def POST(self, username, password):
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            c.execute("INSERT INTO user_string VALUES (?, ?)",
                      [username, password])
        return some_string

def setup_database():
    """
    Create the `user` table in the database
    on server startup
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE user (username, password, calendar_url, timezone, walking_speed)")

def cleanup_database():
    """
    Destroy the `user` table from the database
    on server shutdown.
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE user")

if __name__ == '__main__':
    conf = {
        '/': {
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
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = MatkaClient()
    webapp.service = MatkaService()
    cherrypy.quickstart(webapp, '/', conf)