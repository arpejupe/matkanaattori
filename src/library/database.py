# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import time

from config import constant

class Database(object):

    def setup(self):
        with sqlite3.connect(constant.DB) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE user (user_id, username, password, timezone, walking_speed)")
            cur.execute("CREATE TABLE calendar_url (user_id, url)")

    def cleanup(self):
        with sqlite3.connect(constant.DB) as con:
            cur = con.cursor()
            cur.execute("DROP TABLE user")
            cur.execute("DROP TABLE calendar_url")
