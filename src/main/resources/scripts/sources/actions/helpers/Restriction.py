from base.Container import Container

class Restriction(Container):
    
    _message = "Zaakceptowany"
    
    def canProceed(self):
        return False
    
    def getTemplateName(self):
        return "unset"
    
    def getMessage(self):
        return self._message