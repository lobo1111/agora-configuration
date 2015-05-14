from pl.reaper.container.data import BankNote
from base.Container import Container

class BankNoteManager(Container):

    def create(self):
        note = BankNote()
        note.setPossession(self.findById("Possession", self._svars.get('possessionId')))
        note.setElement(self.findById("Element", self._svars.get('elementId')))
        note.setCreatedAt(self.parseDate(self._svars.get('createdAt')))
        note.setNoteValue(float(self._svars.get('value')))
        note.setDescription(self._svars.get('description'))
        self.saveEntity(note)