# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#

DB_STRING = "matkanaattori.db"

import cherrypy
import sqlite3

def check_credentials(username, password):
    
    with sqlite3.connect(DB_STRING) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE username=:username AND password=:password", 
                    {'username': username, 'password': password})
        result = cur.fetchone()
        if result is None: 
            return u"Incorrect username or password." 
        else:
            return None
        

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/")
        else:
            raise cherrypy.HTTPRedirect("/")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

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