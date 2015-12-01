import snappy
import location_pb2
from location_pb2 import Response

URL = "http://jyulocation.appspot.com/locate/Ag%20Alfa"

from requests import get

message = Response()
r = get(URL, stream=True)
uncomp = snappy.uncompress(r.content)
message.ParseFromString(uncomp)

print (message.status) # found: 0, not found: 1, error: 2

for l in message.location:
    print (l.lat)
    print (l.lng)
