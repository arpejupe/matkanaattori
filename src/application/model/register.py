# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import time

from pyvalidate import validate, ValidationException
from cgi import escape
from config import constant

class SubmitException(Exception):
    pass

class DatabaseError(Exception):
    pass

class RegisterModel(object):

    def insert_user(self, username, password, timezone, calendar_url):
        try:
            with sqlite3.connect(constant.DB) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
                          [username, password, timezone, calendar_url])

        except sqlite3.Error, e:
            raise DatabaseError(e)

    @validate(requires=['username', 'password', 'timezone', 'calendar_url'],
              values= {'calendar_url': '^https?://'})
    def validate_user(self, username, password, timezone, calendar_url):
        pass

    def submit(self, username, password, timezone, calendar_url):
        username = escape(username)
        password = escape(password)
        timezone = escape(timezone)
        calendar_url = escape(calendar_url)

        try:
            self.validate_user(username=username, password=password, timezone=timezone, calendar_url=calendar_url)
        except ValidationException as ex:
            raise SubmitException(ex.message)

        try:
            self.insert_user(username, password, timezone, calendar_url)
        except DatabaseError as ex:
            raise SubmitException("Registration failed please try again!")
