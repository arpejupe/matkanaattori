# -*- coding: utf-8 -*-

import cherrypy
import sqlite3

from config import constant

def get_info(user_id):
    
    with sqlite3.connect(constant.DB) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE user_id=:user_id", 
                    {'user_id': user_id})
        user_info = cur.fetchone()
        
        cur.execute("SELECT url FROM calendar_url WHERE user_id=:user_id", 
                    {'user_id': user_id})
        calendar_info = cur.fetchall()
        
        return {"user_id": user_info[0],
                "username": user_info[1],
                "timezone": user_info[3],
                "walkspeed": user_info[4],
                "calendar_url": calendar_info}