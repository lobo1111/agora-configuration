from base.Container import Container
from structures.helpers.person.Mapper import PersonMapper

class PersonManager(Container):
    _mapper = PersonMapper()
    
    def set(self, entity):
        self._mapper.extractOrCreatePerson(entity)
        self._mapper.setData()
        entity.setPerson(self._mapper.getEntity())
        
    def getMapper(self):
        return self._mapper
    
    