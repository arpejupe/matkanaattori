from urllib import urlencode
from xml.etree import ElementTree
from requests import get
from datetime import datetime

matka_api = "http://api.matka.fi/?"
api_user = "matkanaattori"
api_pass = "ties532soa"

def getRouteDepartureTime(a, b, time, walkspeed, timemode="2", show="1"):
    params = urlencode({
            "a": a, # start point
            "b": b, # destination point
            "time": time, # time of arrival
            "timemode": timemode, # 1: time is the time of departure, 2: the time of arrival
            "show": show, # number of valid routing results
            "walkspeed": walkspeed, # walking speeds 1,2,3,4,5
            "user": api_user, # API user name
            "pass": api_pass # API password
        })
    r = get(matka_api + params, stream=True)
    if r.status_code is 200:
        r.raw.decode_content = True
        events = ElementTree.iterparse(r.raw)
        for elem,event in events:
            if event.tag == "DEPARTURE":
                departure_date = event.attrib["date"]
                departure_time = event.attrib["time"]
                return datetime.strptime(departure_date + departure_time, "%Y%m%d%H%M")
    return None

if __name__ == '__main__':
    departure_time = getRouteDepartureTime("3597369,6784330", "3392009,6686355", "1030", "2")
    print departure_time
