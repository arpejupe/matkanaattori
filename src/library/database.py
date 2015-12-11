# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import time
from config import constant

class Database(object):

    def setup(self):
        with sqlite3.connect(constant.DB) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE user (username, password, timezone, calendar_url)")

    def cleanup(self):
        with sqlite3.connect(constant.DB) as con:
            cur = con.cursor()
            cur.execute("DROP TABLE user")
