# -*- coding: utf-8 -*-
import logging

from ddsw_chat.contrib import Singleton 



@Singleton
class ChatRoom(object):
    """ Repräsentiert den Chat-Room und hat die Aufgabe die Benutzer zu
    verwalten und Nachrichten an diese zu verteilen. """

    def __init__(self):
        logging.info(u"Created new ChatRoom '%s'." % self)
        self.clients = set()
    
    
    def __unicode__(self):
	""" Gibt den Namen des Chatrooms zurück. Wird momentan nicht
        genutzt. """
        return "default"
    
    
    def join(self, client):
	""" Registriert einen neuen Client im Chatroom und publizieret dies
        an die bereits registrierten Clients. """
        logging.info(u"'%s' joins ChatRoom '%s'." % (client, self))
        self.response_to_all("user_joins", name=unicode(client))
        self.clients.add(client)
        self.send_user_list()
    
    
    def leave(self, client):
	""" Entfernt einen Client im Chatroom und publizieret dies an die
        bereits registrierten Clients. """
        logging.info(u"'%s' leaves ChatRoom '%s'." % (client, self))
        self.clients.remove(client)
        self.response_to_all("user_leaves", name=unicode(client))
        self.send_user_list()
    
    
    def send_user_list(self):
        """ Sendet eine komplette Benutzerliste an alle Clients. """
        users = [unicode(u) for u in self.clients]
        self.response_to_all("refresh_user_list", users=users)
    
    
    def response_to_all(self, event, **kwargs):
        """ Hilfsmethode um eine Nachricht an alle Clients zu senden. """
        for client in self.clients:
            client.response(event, **kwargs)
    
    
    def new_message(self, client, message):
        """ Sendet eine Chatnachricht an alle Clients. """
        logging.info(u"New message from '%s': %s" % (client, message))
        self.response_to_all("new_message", name=unicode(client), message=message)


