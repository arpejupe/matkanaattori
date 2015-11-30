import cherrypy
import requests

#for debugging
from pprint import pprint

class Matka(object):
    @cherrypy.expose
    def index(self):
        return "Welcome using matkanaattori!"

    @cherrypy.expose
    def locate(self, start, destination):
        # http://api.matka.fi/?a=3597369,6784330&b=3392009,6686355&user=matkanaattori&pass=ties532soa
        response = requests.get("http://api.matka.fi/?a=" + start + "&b=" + destination + "&user=matkanaattori&pass=ties532soa")
        xml = response.text
        cherrypy.response.headers["Content-Type"] = "text/xml; charset=utf-8"
        return xml

if __name__ == '__main__':
    cherrypy.quickstart(Matka())