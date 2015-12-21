# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import time

from application.model import user
from cgi import escape
from config import constant

class SubmitException(Exception):
    pass

class DatabaseError(Exception):
    pass

class SettingsModel(object):

    def update_user(self, id, timezone, walking_speed, calendar_url):
        try:
            with sqlite3.connect(constant.DB) as con:
                
                cur = con.cursor()
                
                cur.execute("UPDATE user SET timezone=:timezone, walking_speed=:walking_speed WHERE user_id=:user_id",
                            {"timezone": timezone, "walking_speed": walking_speed, "user_id": id})
                            
                cur.execute("DELETE FROM calendar_url WHERE user_id =:user_id", 
                            {"user_id": id})  
                            
                for url in calendar_url:
                    cur.execute("INSERT INTO calendar_url VALUES (?, ?)",
                                [id, url])        
                                
        except sqlite3.Error, e:
            cherrypy.log(e.message, traceback=True)
            raise DatabaseError(e)

    def submit(self, id, timezone, walking_speed, calendar_url):
        
        # Filter empty fields from the list
        calendar_url = filter(None, calendar_url)
        
        # Go through list to escape
        i=0
        for url in calendar_url:
            calendar_url[i] = escape(url)
            i=+1
            
        try:
            self.update_user(id, timezone, walking_speed, calendar_url)
            userinfo = user.get_info(id)
            cherrypy.session.regenerate()      
            cherrypy.session[constant.SESSION_KEY] = userinfo
        except DatabaseError as ex:
            raise SubmitException("Settings update failed please try again!")
