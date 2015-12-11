import snappy
import cgi
import cachetools
from library.location_pb2 import *
from requests import get

URL = "http://jyulocation.appspot.com/locate/"

@cachetools.func.lru_cache(maxsize=32)
def getJyuLocation(locationName):
    message = Response()
    r = get(URL + cgi.escape(locationName), stream=True)
    u = snappy.uncompress(r.content)
    message.ParseFromString(u)

    #print (message.status) # found: 0, not found: 1, error: 2

    if message.status is 0:
        return message.location[0]
    return None

if __name__ == '__main__':
    for x in range(0, 4):
        location = getJyuLocation("Ag Alfa")
        print ("Location of Ag Alfa:")
        print (location.lat)
        print (location.lng)
        location = getJyuLocation("Ag Gamma")
        print ("Location of Ag Gamma:")
        print (location.lat)
        print (location.lng)
    print(getJyuLocation.cache_info())
