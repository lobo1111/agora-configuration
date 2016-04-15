from java.util import Date
from pl.reaper.container.data import Note
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.LengthValidator import LengthValidator

class NoteMapper(Mapper):
    
    def initStructure(self):
        if int(self.get('id')) > 0:
            self._logger.info("Note persist - it's an update. Found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Note", int(self._svars.get('id')))
            self._isNewStructure = False
            return self._entity
        else:
            self._logger.info("Note persist - it's a new note")
            self._isNewStructure = True
            self._entity = Note()
            return self._entity

    def setData(self):
        self.map("title", [LengthValidator(minLength=1, maxLength=150, messageParameter=self._label.get('field.noteTitle'))])
        self.map("note")
    
    def isNew(self):
        return self._isNewStructure
    
    def setUser(self, user):
        self._entity.setPerson(user)
        
    def setDate(self):
        self._entity.setDate(Date())
        
    def markAsRemoved(self):
        self._entity.setRemoved(True)
        