# -*- coding: utf-8 -*-

import snappy
import cgi
import cachetools
from library.location_pb2 import *
from requests import get

from config import constant

class JyuLocationException(Exception):
    pass

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
        location = getJyuLocation("Ag Alfa")
        print ("Location of Ag Alfa:")
        print (location.lat)
        print (location.lng)
        location = getJyuLocation("Ag Gamma")
        print ("Location of Ag Gamma:")
        print (location.lat)
        print (location.lng)
    print(getJyuLocation.cache_info())
