__author__ = 'bob'

import cherrypy
import os
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
        html_dir = os.path.dirname(os.path.abspath(__file__)) + "/html/"
        css_dir = html_dir + "css/"
        img_dir = html_dir + "img/"
        js_dir = html_dir + "js/"
        config = {'/css':
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
        #~ cherrypy.tree.mount(Root(), '/', config=config)
        cherrypy.quickstart(Root(), '/', config=config)
        #~ cherrypy.quickstart(Root())


class Root:

    @expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render(salutation="Hello", target="World", version="0.0.1")

    @expose
    def config(self):
        tmpl = lookup.get_template("config.html")
        return tmpl.render(version="0.0.1")

    @expose
    def showMessage(self):
        return "Hello world!"

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

def main():
    #~ current_dir = os.path.dirname(os.path.abspath(__file__)) + "/html/"
    #~ cherrypy.config.update({
        #~ 'log.screen': True,
        #~ 'server.socket_host': '127.0.0.1',
        #~ 'server.socket_port': 10307,
        #~ 'server.shutdown_timeout': 0,
        #~ 'engine.autoreload_on': True,
        #~ '/':{
            #~ 'tools.staticdir.debug': True,
            #~ 'log.screen': True,
            #~ 'tools.staticdir.root' : current_dir,
            #~ },
        #~ '/css':{
            #~ 'tools.staticdir.debug': True,
            #~ 'log.screen': True,
            #~ 'tools.staticdir.on' : True,
            #~ 'tools.staticdir.dir' : "css",
        #~ },
    #~ })
    server = UIServer()
    server.start()
    return 0

if __name__ == "__main__":
    main()
