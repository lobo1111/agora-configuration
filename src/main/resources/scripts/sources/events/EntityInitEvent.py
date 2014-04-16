from events.Event import Event
from helpers.Initializator import Initializator

class EntityInitEvent(Event):
    def run(self):
        object = Initializator().objectInitialize(self._session.getParameter("classPath"))
        self._session.setParameter("entity", object)