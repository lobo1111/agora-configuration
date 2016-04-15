from base.Container import Container
from structures.helpers.note.Mapper import NoteMapper
from structures.validators.common.ValidationError import ValidationError

class NoteManager(Container):
    _mapper = NoteMapper()
    
    def persist(self):
        try:
            self._mapper.initStructure()
            self._mapper.setData()
            if self._mapper.isNew():
                self._mapper.setUser(User().collectUser())
                self._mapper.setDate()
            self.saveEntity(self._mapper.getEntity())
        except ValidationError, e:
            self.setError(e)
            
    def remove(self):
        try:
            self._mapper.initStructure()
            self._mapper.markAsRemoved()
            self.saveEntity(self._mapper.getEntity())
        except ValidationError, e:
            self.setError(e)