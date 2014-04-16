from events.Event import Event
from helpers.Entity import Entity

class EntityPersistEvent(Event):
    def run(self):
        Entity().persist(self._session.getParameter("entity"))