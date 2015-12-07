DB_STRING = "matkanaattori.db"

import cherrypy
import sqlite3
import time

from pyvalidate import validate, ValidationException
from cgi import escape

from pyvalidate import validate, ValidationException

class SubmitException(Exception):
    pass

def setup_database():
    with sqlite3.connect(DB_STRING) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE user (username, password, timezone, calendar_url)")

def cleanup_database():
    with sqlite3.connect(DB_STRING) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE user")

def insert_user(username, password, timezone, calendar_url):
    try:
        with sqlite3.connect(DB_STRING) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
                      [username, password, timezone, calendar_url])
                      
    except sqlite3.Error, e:
        raise DatabaseError(e)

@validate(requires=['username', 'password', 'timezone', 'calendar_url'],
          values= {'calendar_url': '^https?://'})
def validate_user(username, password, timezone, calendar_url):
    pass

def submit(username, password, timezone, calendar_url):
    username = escape(username)
    password = escape(password)
    timezone = escape(timezone)
    calendar_url = escape(calendar_url)
    
    try:
        validate_user(username=username, password=password, timezone=timezone, calendar_url=calendar_url)
    except ValidationException as ex:
        raise SubmitException(ex.message)
    
    try:
        insert_user(username, password, timezone, calendar_url)
    except DatabaseError as ex:
        raise SubmitException("Registration failed please try again!")


cherrypy.engine.subscribe('start', setup_database)
cherrypy.engine.subscribe('stop', cleanup_database)