# -*- coding: utf-8 -*-
"""
Enthält die Klasse für die logische Representation eines Chatclients.
"""

import logging


from ddsw_chat.exceptions import ChatError
from ddsw_chat.errorcodes import UNKNOWN_EVENT
from ddsw_chat.contrib import generate_name
from ddsw_chat.room import ChatRoom



class ChatClient(object):
    """ Logische Representation eines Chatclients.
    
    Diese Klasse wird vom (indirekt) ChatWebSocket aufgerufen und kümmert sich
    um die Abarbeitung der Events. Außerdem meldet sie sich im ChatRoom an
    und wieder ab.
    
    Methoden dieser Klasse werden im Thread vom Worker ausgeführt (ausgenommen
    open und close). Daher ist die Klasse größtenteils threadsafe.
    """
    
    def __init__(self, ws):
        self.ws = ws
        self.name = generate_name()

        logging.info(u"New connection from '%s'." % self)
        self.room = ChatRoom.Instance() #@UndefinedVariable (class decorator)
        self.room.join(self)
    
    
    def __unicode__(self):
        """ Eine textuelle Representation des Clients. """
        return self.name
    
    
    
    def close(self):
        """ Handler für das Schließen der Verbindung. """
        self.room.leave(self)
        logging.info(u"Closed connection from '%s'." % self)
    
    
    def response(self, event, **kwargs):
        """ Shortcut an den Websocket. """
        self.ws.response(event, **kwargs)

    
    def request(self, event, **kwargs):
        """ Handler für ankommende Requests vom Socket.
        
        Wertet das 'event' aus und versucht die entsprechende Methode dieser
        Klasse aufzurufen (on_ Präfix).
        """
        try:
            method = getattr(self, "on_%s" % event)
        except AttributeError:
            msg = "Unknown event '%s'." % event
            code = UNKNOWN_EVENT
            raise ChatError(code, msg)
        
        method(**kwargs)
    
    
    def on_send(self, message):
        """ Handler für 'send'-Event (ankommende Nachrichen. """
        self.room.new_message(self, message)

    
        