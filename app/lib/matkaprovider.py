from urllib import urlencode
from xml.etree import ElementTree
from requests import get
from datetime import datetime

matka_api = "http://api.matka.fi/?"

class Matkaprovider(object):
    def __init__(self, user, pw):
        self.user = user
        self.pw = pw

    def getRouteDepartureTime(self, a, b, time, walkspeed, timemode="2", show="1"):
        params = urlencode({
                "a": a, # start point
                "b": b, # destination point
                "time": time, # time of arrival
                "timemode": timemode, # 1: time is the time of departure, 2: the time of arrival
                "show": show, # number of valid routing results
                "walkspeed": walkspeed, # walking speeds 1,2,3,4,5
                "user": self.user,
                "pass": self.pw
            })
        r = get(matka_api + params, stream=True)
        r.raw.decode_content = True
        events = ElementTree.iterparse(r.raw)
        for elem,event in events:
            if event.tag == "DEPARTURE":
                date = event.attrib["date"]
                departuretime = event.attrib["time"]
                return datetime.strptime(date+time,"%Y%m%d%H%M")
        return None

if __name__ == '__main__':
    matka = Matkaprovider("matkanaattori", "password")
    start = matka.getRouteDepartureTime("3597369,6784330", "3392009,6686355", "1030", "2")
    print start
