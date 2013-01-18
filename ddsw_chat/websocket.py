# -*- coding: utf-8 -*-
"""
Enthält den Handler für neue Websocketverbindungen.
"""

import json
import logging


import tornado.websocket


from ddsw_chat.worker import worker
from ddsw_chat.client import ChatClient
from ddsw_chat.exceptions import ChatError



class ChatWebSocket(tornado.websocket.WebSocketHandler):
    """ Handler für Websocketverbindungen.
    
    Diese Klasse implementiert den Tornado-Handler für neue
    Websocketverbindungen. D.h., dass es für jede neue Verbindung eine neue
    Instanz dieser Klasse erstellt wird.
    
    Er implementiert die Methoden 'open()', 'on_close()' und 'on_message()',
    als Schnittstellen vom Webserver.
    
    Außerdem bietet er die Methode 'response()' an umd einen threadsicheren
    Kanal zum Socket zu bieten.
    """
    
    def open(self): #@ReservedAssignment
        """ Handler für neue Verbindungen.
        
        Erstellt einen neuen Client.
        """
        self.client = ChatClient(self)


    def on_close(self):
        """ Handler für das Beenden einer Verbindung.
        
        Teilt dem Client mit, dass die Verbindung geschlossen wird und löscht
        diesen dann, damit er (hoffentlich) vom Garbarge-Collector gelöscht
        wird.
        """
        if hasattr(self, "client"):
            self.client.close()
            del self.client

    
    def on_message(self, message):
        """ Handler für neue eintreffende Nachrichten.
        
        Dieser Handler wandelt den JSON-String in ein Objekt um und teilt dem
        Worker mit, dass er die neue Nachricht abarbeiten soll.
        """
        try:
            request = json.loads(message)
            event = request.pop('event')
            worker.add(self.client.request, args=(event,), kwargs=request)

        except Exception, e:
            self.exception_response(e)
    

    def write_message(self, message):
        """ Erweiterung der Basisklasse um Fehler abzufangen. """
        try:
            super(ChatWebSocket, self).write_message(message)
        except Exception:
            logging.error("Exception on writing message!")
    
    
    def response(self, event, **kwargs):
        """ Schnittstelle um threadsicher Responses an den Socket zu senden.
        
        Dazu wird ein Callback (closure) and den IOLoop gesendet, damit er in
        der nächsten Iteration abgearbeitet werden kann. """
        def callback():
            if self is None:
                return
            kwargs['event'] = event
            try:
                message = json.dumps(kwargs)
                self.write_message(message)
            except Exception, e:
                self.exception_response(e)
            
        tornado.ioloop.IOLoop.instance().add_callback(callback)
        
     
    def exception_response(self, e):
        """Propagieren von Fehlern.
        
        Sollte in der Abarbeitung von Nachrichten Fehler auftreten, so schreibt
        diese Methode diese in den Logger und an den Socket."""
        logging.error("%s: %s" % (e.__class__.__name__, e))
        if isinstance(e, ChatError):
            self.write_message(json.dumps({
                'event': 'error',
                'message': unicode(e),
                'code': e.code,
            }))
        else:
            self.write_message(json.dumps({
                'event': 'exception',
                'message': unicode(e),
            }))
    