# -*- coding: utf-8 -*-

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
import json
import datetime
import pytz

from lib import calendarprovider
from lib import coordinates
from lib import jyulocation
from lib import matkaprovider

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
        
    #@cherrypy.tools.mako(filename="locate.html")
    @cherrypy.expose
    def locate(self, username, lat=None, lng=None):
        with sqlite3.connect(DB_STRING) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM user WHERE username=:username", 
                        {'username': username})
            result = cur.fetchone()
            calendar_url = result[3]
        # annettu: käyttäjänimi ja käyttäjän geolokaatio
        # pyydä: käyttäjän kalenter(e)ista next eventin aloitusaika
        # muuta: next eventin paikka koordinaateiksi
        # muuta: koordinaatit kkj3:ksi
        # välitä: matka.fi:in tapahtuman aloitusaika (HHMM), lähtö ja määränpään koordinaatit (a, b)
        # vastaus: lähtöaika
        # laske: lähtöaika - nykyaika = aikaa jäljellä (huomio eventin sattuminen eri päivälle)
        # palauta: aikaa jäljellä
        # testi url: localhost:8080/locate/juha?lat=64.2261178&lng=27.7306952
        nextEvent = calendarprovider.getNextEvent(calendar_url)
        event_location = jyulocation.getJyuLocation(nextEvent["location"])
        kkj3_event_location = coordinates.WGS84lalo_to_KKJxy({"La": event_location.lat,
                                                              "Lo": event_location.lng})
        kkj3_geolocation = coordinates.WGS84lalo_to_KKJxy({"La": float(lat),
                                                           "Lo": float(lng)})
        a = "{0},{1}".format(int(kkj3_geolocation["I"]), int(kkj3_geolocation["P"]))
        b = "{0},{1}".format(int(kkj3_event_location["I"]), int(kkj3_event_location["P"]))
        # vaihda käyttäjän valitsema aikavyöhyke tähän
        usertimezone = pytz.timezone("Europe/Helsinki")
        arrival_time = nextEvent["startTime"].astimezone(usertimezone)
        # hae walkspeed käyttäjän tiedoista
        walkspeed = 3
        departure_time = matkaprovider.getRouteDepartureTime(a, b, arrival_time, walkspeed)
        timeLeft = departure_time - datetime.datetime.now()
        return json.dumps({'result': timeLeft.seconds})

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
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
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
