# -*- coding: utf-8 -*-

import sys
import os, os.path
import cherrypy

from config import constant

#for debugging
from pprint import pprint

class Main(object):

    def __init__(self, options):

        # First let's see where we're located
        self.base_dir = os.path.normpath(os.path.abspath(options.basedir))

        # Our config directory
        self.conf_path = os.path.join(self.base_dir, "config")

        # Create the logs directory
        log_dir = os.path.join(self.base_dir, "log")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        # Update the global settings for the HTTP server and engine
        cherrypy.config.update(os.path.join(self.conf_path, "server.cfg"))
        cherrypy.config.update({'error_page.default': self.on_error})

        # We amend the system path so that Python can find
        # the application's modules.
        sys.path.insert(0, self.base_dir)

        # Set the priority according to your needs if you are hooking something
        # Else on the 'before_finalize' hook point.
        cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', self.secureheaders, priority=60)

        # Set constants
        constant.DB = "matkanaattori.db"
        constant.SESSION_KEY = "_cp_user"
        constant.SALT = "javaninjat2015" # could be anything you like
        constant.JYULOCATION = "http://jyulocation.appspot.com/locate/" # restful web service to convert locations

        # Template engine tool
        from library.template import MakoLoader
        cherrypy.tools.mako = cherrypy.Tool('on_start_resource', MakoLoader())

        # Load controllers for our application
        from application.controller.auth import LoginController, LogoutController
        from application.controller.register import RegisterController
        from application.controller.settings import SettingsController
        from application.controller.location import LocationController

        controllers = {"login": LoginController(),
                       "logout": LogoutController(),
                       "register": RegisterController(),
                       "settings": SettingsController(),
                       "location": LocationController()}

        # Inject them to index controller
        from application.controller.index import IndexController
        application = IndexController(controllers)

        # Let's mount the application so that CherryPy can serve it
        application = cherrypy.tree.mount(application, '/', os.path.join(self.conf_path, "app.cfg"))

        # Load database library
        from library.database import Database
        database = Database()

        # Start database by using start and clean it using stop. Comment these after initialization
        #cherrypy.engine.subscribe('stop', database.cleanup)
        #cherrypy.engine.subscribe('start', database.setup)

    def run(self):
        engine = cherrypy.engine

        if hasattr(engine, "signal_handler"):
            engine.signal_handler.subscribe()

        if hasattr(engine, "console_control_handler"):
            engine.console_control_handler.subscribe()

        # Let's start the CherryPy engine so that
        # everything works
        engine.start()

        # Run the engine main loop
        engine.block()

    def secureheaders(self):
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['Content-Security-Policy'] = "default-src='self'"

    def on_error(self, status, message, traceback, version):
        code = '404' if status.startswith('404') else 'error'
        template = cherrypy.engine.publish('lookup-template', "%s.mako" % code).pop()
        return template.render()

if __name__ == '__main__':

    from optparse import OptionParser

    def parse_commandline():
        curdir = os.path.normpath(os.path.abspath(os.path.curdir))
        parser = OptionParser()
        parser.add_option("-b", "--base-dir", dest="basedir",
                          help="Base directory in which the server "\
                          "is launched (default: %s)" % curdir)
        parser.set_defaults(basedir=curdir)
        (options, args) = parser.parse_args()

        return options

    Main(parse_commandline()).run()
