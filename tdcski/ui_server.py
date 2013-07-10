#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2013 Bob <TDC-bob@daribouca.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import tdcski
import cherrypy
import os
import sys
import threading
import webbrowser
from tdcski import alerts
from tdcski.network_interfaces import all_interfaces_html
import tdcski.config_handler
from cherrypy import expose, tools
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

class UIServer():
    def __init__(self):
        cherrypy.server.shutdown_timeout = 0
        cherrypy.server.socket_port = int(tdcski.config.server.port)
        cherrypy.server.socket_host = tdcski.config.server.interface

    def start(self):
        def fake_wait_for_occupied_port(host, port): return
        cherrypy.process.servers.wait_for_occupied_port = fake_wait_for_occupied_port
        cherrypy.engine.timeout_monitor.unsubscribe()
        html_dir = tdcski.config.path_to.own_dir + "/html/"
        css_dir = html_dir + "css/"
        img_dir = html_dir + "img/"
        js_dir = html_dir + "js/"
        server_config = {'/css':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': css_dir,
                },
                '/img':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': img_dir,
                },
                '/js':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': js_dir,
                },
                '/static':
                {'tools.staticdir.on': True,
                 'tools.staticdir.dir': html_dir,
                }
        }
        cherrypy.engine.autoreload.unsubscribe()
        cherrypy.quickstart(Root(), '/', config=server_config)


class Root:

    @expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render(
            salutation="Hello",
            target="World",
            version=tdcski.version,
            alerts=tdcski.alerts.get_alerts(),
        )

    @expose
    def show_config(self):
        tmpl = lookup.get_template("config.html")
        return tmpl.render(
            version=tdcski.version,
           server_interface=tdcski.config.server.interface,
           server_port=tdcski.config.server.port,
           dcs_path=tdcski.config.path_to.DCS,
           saved_games=tdcski.config.path_to.saved_games,
           interfaces=all_interfaces_html(),
           alerts=tdcski.alerts.get_alerts()
        )

    @expose
    def save_config(self, **kwargs):
        print(kwargs)
        tdcski.config.server.interface = kwargs["server_interface"]
        tdcski.config.server.port = kwargs["server_port"]
        tdcski.config.path_to.DCS = kwargs["dcs_dir"]
        tdcski.config.path_to.saved_games = kwargs["saved_games"]
        raise cherrypy.HTTPRedirect("/show_config")

    @expose
    def showMessage(self):
        return "Hello world!"

    @expose
    def exit(self):
        tmpl = lookup.get_template("exit.html")
        threading.Timer(1, lambda: os._exit(0)).start()
        return tmpl.render(
            version=tdcski.version,
            alerts=tdcski.alerts.get_alerts()
        )

    @expose
    def user(self, name=""):
        return "You asked for user '%s'" % name

    @expose
    def test_receive(self, user='', pwd=''):
        print("user: {}".format(user), "pwd: {}".format(pwd))
        return self.user(user)
        #~ raise cherrypy.HTTPRedirect("/")

    @expose
    def default(self, *args):
        raise cherrypy.HTTPRedirect("/")
        return "Caribou ! Lien invalide: {}".format("/".join(args))

    @expose
    def do_update(self):
        return "updating, sir !"

def main():
    server = UIServer()
    threading.Timer(2, lambda: webbrowser.open("http://127.0.0.1:{}".format(tdcski.config.server.port), new=2, autoraise=True)).start()
    server.start()
    return 0

if __name__ == "__main__":
    sys.exit(main())
