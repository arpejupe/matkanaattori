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
        result = cur.fetchall()

        calendar_url=[]
        for url in result:
            calendar_url.append(url[0])

        return {"user_id": user_info[0],
                "username": user_info[1],
                "timezone": user_info[3],
                "walkspeed": user_info[4],
                "calendar_url": calendar_url}