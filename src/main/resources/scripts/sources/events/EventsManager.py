from helpers.Initializator import Initializator
from event.Session import Session

class EventsManager:
    
    def callEvent(self, eventName, session):
        event = self.loadEvent(eventName)
        for action in event.actions:
            self.callAction(action, session)
            
    def loadEvent(self, eventName):
        pass
    
    def callAction(self, action, session):
        for parameter in action.getParameters():
            session.setParameter(parameter.getName(), parameter.getValue())
        if action.getType() == "event":
            self.callEvent(action.getHandler(), session)
        else:
            self.callScript(action.getHandler(), session)
            
    def callScript(self, scriptName, session):
        object = Initializator().objectInitialize(scriptName)
        object.setSession(session)
        object.run()
        
    def startEventsChain(self, eventName, svars):
        self.callEvent(eventName, Session(svars))