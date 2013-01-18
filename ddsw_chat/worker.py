# -*- coding: utf-8 -*-
"""
Enthält die Klasse für den Worker.
"""

import threading
import Queue



class RequestWorker(threading.Thread):
    """ Der RequestWorker arbeitet alle Nachrichten ab. """
    
    def __init__(self):
        self.queue = Queue.Queue()
        
        super(RequestWorker, self).__init__()
        self.daemon = True
    
    
    def run(self):
        """ Startet den Worker, arbeitet alle Aufgaben ab und blockiert bis
        neue Aufgaben eintreffen. """
        while True:
            method, args, kwargs = self.queue.get()
            method(*args, **kwargs)
            self.queue.task_done()
        
    
    def add(self, method, args, kwargs):
        """ Fügt eine neue Aufgabe hinzu. """
        item = (method, args, kwargs)
        self.queue.put(item)



worker = RequestWorker()
worker.start()
