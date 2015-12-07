DB_STRING = "matkanaattori.db"

import cherrypy
import sqlite3
import time

def setup_database():
    with sqlite3.connect(DB_STRING) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE user (username, password, timezone, calendar_url)")

def cleanup_database():
    with sqlite3.connect(DB_STRING) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE user")
        
def submit(username, password, timezone, calendar_url):
    with sqlite3.connect(DB_STRING) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
                  [username, password, timezone, calendar_url])
    return True

cherrypy.engine.subscribe('start', setup_database)
cherrypy.engine.subscribe('stop', cleanup_database)