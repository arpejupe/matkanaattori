# -*- coding: utf-8 -*-

import snappy
import cgi
import cachetools
from library.location_pb2 import *
from requests import get

from config import constant

class JyuLocationException(Exception):
    pass

class JyuLocation(object):
    def __init__(self, location_name):
        self.name = location_name
        self.coordinates = getJyuLocation(self.name)

@cachetools.func.lru_cache(maxsize=32)
def getJyuLocation(location_name):
    message = Response()
    response = get(constant.JYULOCATION + cgi.escape(location_name), stream=True)
    data = snappy.uncompress(response.content)
    message.ParseFromString(data)

    #print (message.status) # found: 0, not found: 1, error: 2
    if message.status is 0:
        return message.location[0]
    raise JyuLocationException("Jyu location not available for %s" % location_name)

if __name__ == '__main__':
    for x in range(0, 4):
        agAlfa = JyuLocation("Ag Alfa")
        print ("Location of Ag Alfa:")
        print (agAlfa.coordinates.lat)
        print (agAlfa.coordinates.lng)
        agGamma = JyuLocation("Ag Gamma")
        print ("Location of Ag Gamma:")
        print (agGamma.coordinates.lat)
        print (agGamma.coordinates.lng)
    print(getJyuLocation.cache_info())
