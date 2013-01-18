

class ChatException(Exception):
    pass


class ChatError(ChatException):
    def __init__(self, code, msg):
        self.message = msg
        self.code = code
    
    def __unicode__(self):
        return self.message
    
    def __str__(self):
        return self.message