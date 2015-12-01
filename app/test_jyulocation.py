import snappy
import cgi
import location_pb2
from location_pb2 import Response
from requests import get

URL = "http://jyulocation.appspot.com/locate/"

def getJyuLocation(classroom):
    message = Response()
    r = get(URL + cgi.escape(classroom), stream=True)
    uncomp = snappy.uncompress(r.content)
    message.ParseFromString(uncomp)

    #print (message.status) # found: 0, not found: 1, error: 2

    if message.status is 0:
        return message.location[0]
    return None

if __name__ == '__main__':
    location = getJyuLocation("Ag Alfa")
    print ("Location of Ag Alfa:")
    print (location.lat)
    print (location.lng)

