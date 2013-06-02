__author__ = 'bob'

import cherrypy
from cherrypy import expose
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

class UIServer():
    def __init__(self):
        cherrypy.server.shutdown_timeout = 0
        cherrypy.server.socket_port = 10307
        cherrypy.server.socket_host = "127.0.0.1"

    def start(self):
        def fake_wait_for_occupied_port(host, port): return
        cherrypy.process.servers.wait_for_occupied_port = fake_wait_for_occupied_port
        cherrypy.engine.timeout_monitor.unsubscribe()
        cherrypy.quickstart(Root())


class Root:

    @expose
    def index(self):
        # Let's link to another method here.
        tmpl = lookup.get_template("index.html")
        return tmpl.render(salutation="Hello", target="World")

    @expose
    def showMessage(self):
        # Here's the important message!
        return "Hello world!"

    @expose
    def user(self, name=""):
        return "You asked for user '%s'" % name

    @expose
    def receive(self, user='', pwd=''):
        print("user: {}".format(user), "pwd: {}".format(pwd))

    @expose
    def default(self, *args):
        return "Caribou ! Lien invalide: {}".format("/".join(args))