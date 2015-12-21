# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import time
import hashlib, uuid

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
                id = str(uuid.uuid4())
                password = hashlib.sha512(password + constant.SALT).hexdigest()
                walking_speed = "3";
                cur = con.cursor()
                cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)",
                            [id, username, password, timezone, walking_speed])
                for url in calendar_url:
                    cur.execute("INSERT INTO calendar_url VALUES (?, ?)",
                                [id, url])
        except sqlite3.Error, e:
            raise DatabaseError(e)

    # notice that validator does not function properly because calendar_url is list
    @validate(requires=['username', 'password', 'timezone', 'calendar_url'],
              values= {'calendar_url': '^https?://'})
    def validate_user(self, username, password, timezone, calendar_url):
        pass

    def check_if_exists(self, username):
        with sqlite3.connect(constant.DB) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM user WHERE username=:username", 
                        {'username': username})
            result = cur.fetchone()
            if result is None:
                pass
            else:
                raise DatabaseError("Registration failed: username already exists!")

    def submit(self, username, password, timezone, calendar_url):
        username = escape(username)
        password = escape(password)
        
        # Filter empty fields from the list
        calendar_url = filter(None, calendar_url)
        
        # Check if totally null
        if not calendar_url:
            calendar_url = [""]

        # Go through list to escape
        i=0
        for url in calendar_url:
            calendar_url[i] = escape(url)
            i=+1
            
        try:
            self.validate_user(username=username, password=password, timezone=timezone, calendar_url=calendar_url[0])
        except ValidationException as ex:
            raise SubmitException(ex.message)

        try:
            self.check_if_exists(username)
        except DatabaseError as ex:
            raise SubmitException(ex.message)

        try:
            self.insert_user(username, password, timezone, calendar_url)
        except DatabaseError as ex:
            raise SubmitException("Registration failed please try again!")
