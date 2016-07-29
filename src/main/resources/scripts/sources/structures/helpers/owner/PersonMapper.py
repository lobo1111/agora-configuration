from pl.reaper.container.data import Owner
from structures.helpers.common.Mapper import Mapper
from structures.Person import PersonManager

class PersonMapper(Mapper):
    
    def initStructure(self):
        self._entity = Owner()
    
    def setData(self):
        PersonManager().set(self._entity)
        
    