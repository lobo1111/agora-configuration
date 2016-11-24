from base.Container import Container

class Restriction(Container):
    
    _result = False
    
    def calculate(self):
        pass
    
    def getResult(self):
        return self._result
    