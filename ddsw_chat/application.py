# -*- coding: utf-8 -*-
"""
Dieses Modul ist der Startpunkt zur Anwendung.

Beim import des Moduls wird die Anwendung bereits in der Variable 'app'
initialisiert. Der Server kann dann durch aufruf von 'app.start()' gestartet
werden.

Der Server wird mittels Tornado betrieben:
  * http://www.tornadoweb.org/
  * http://pypi.python.org/pypi/tornado/2.4
  * http://www.tornadoweb.org/documentation/index.html
  * http://www.tornadoweb.org/documentation/web.html
  * http://www.tornadoweb.org/documentation/websocket.html
  * http://www.tornadoweb.org/documentation/ioloop.html
"""

import os
import logging
import sys


import tornado.httpserver
import tornado.ioloop
import tornado.web


import ddsw_chat
from ddsw_chat.websocket import ChatWebSocket



class ChatApplication(object):
    """ Initialisiert den Server
    
    Diese Klasse initialisiert den Server. Darunter zählen die Tornado und die
    'logger' Konfiguration.
    
    Der HTTP-Server ist so konfiguriert, dass:
      * er einen Redirect von '/' zu 'index.html' hat
      * er unter '/ws' den WebSocket für die HTML5-Anwendung bereitstellt und
      * er alle anderen Anfragen statisch aus dem Verzeichnis 'ressources'
        auslieftert.
        
    Der Logger schreibt alle Ausgaben, bis einschließlich Debugnachrichten, in
    die Standardausgabe.
    
    Diese Klasse wird bereits beim Import des Moduls instanziert. Der Server
    kann durch die Methode 'start()' gestartet werden.
    """
    
    def __init__(self):
        self.application = tornado.web.Application([
            (r"/", tornado.web.RedirectHandler, {"url": "/index.html"}),
            (r'/ws', ChatWebSocket),
            (r"/(.*)", tornado.web.StaticFileHandler,
                {"path": self._get_static_path()}),
        ])
        
        logging.basicConfig(
            level = logging.DEBUG,
            format = "%(asctime)s %(levelname)s: %(message)s",
            stream = sys.stdout,
        )
        
    def _get_static_path(self):
        """Gibt den Pfad zum 'ressources'-Verzeichnis zurück."""
        pkg_dir = os.path.dirname(ddsw_chat.__file__)
        return os.path.join(pkg_dir, "ressources")
    
    
    def start(self, port):
        """Startet den Webserver."""
        http_server = tornado.httpserver.HTTPServer(self.application)
        http_server.listen(port)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            print ""
            print "Exiting"


# Die Instanz der Anwendung.
app = ChatApplication()
