# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import json
import datetime
import pytz

from library import coordinates

from application.model import calendar
from application.model import jyulocation
from application.model import matkaprovider

from config import constant
   
class LocateController(object):

    @cherrypy.expose
    def locate(self, username, lat=None, lng=None):
        with sqlite3.connect(constant.DB) as con:
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
        nextEvent = calendar.getNextEvent(calendar_url)
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