class ValidationError(Exception):

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return unicode(self.value).encode('utf8')