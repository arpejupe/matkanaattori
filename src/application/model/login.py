# -*- coding: utf-8 -*-

import cherrypy
import sqlite3
import hashlib, uuid

from application.model import user
from cgi import escape
from config import constant

class LoginModel(object):

    def check_credentials(self, username, password):
        username = escape(username)
        password = escape(password)
        with sqlite3.connect(constant.DB) as con:
            password = hashlib.sha512(password + constant.SALT).hexdigest()
            cur = con.cursor()
            cur.execute("SELECT * FROM user WHERE username=:username AND password=:password", 
                        {'username': username, 'password': password})
            result = cur.fetchone()
            if result is None: 
                return u"Incorrect username or password." 
            else:
                userinfo = user.get_info(result[0])
                cherrypy.session.regenerate()      
                cherrypy.session[constant.SESSION_KEY] = userinfo

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        userinfo = cherrypy.session.get(constant.SESSION_KEY)
        if userinfo:
            cherrypy.request.login = userinfo['username']
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/")
        else:
            raise cherrypy.HTTPRedirect("/")

cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)