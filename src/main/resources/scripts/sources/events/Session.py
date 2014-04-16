class Session:
    def __init__(self, parameters):
        self._parameters = parameters
        
    def setParameter(self, name, value):
        self._parameters.put(name, value)
        
    def getParameter(self, name):
        return self._parameters.get(name)