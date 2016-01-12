from base.Container import Container

class Restriction(Container):
    
    _message = "Zaakceptowany"
    _result = False
    
    def calculate(self):
        pass
    
    def getResult(self):
        return self._result
    
    def getMessage(self):
        return self._message