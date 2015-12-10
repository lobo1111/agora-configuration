from documents.Document import Document
from pl.reaper.container.data import BankNote
from pl.reaper.container.data import BankNotePosition

class BankNote(Document):
    
    def create(self):
        note = self.initDocument(BankNote(), BankNote.TYPE)
        note.setPossession(self.findById("Possession", self._svars.get('possessionId')))
        note.setElement(self.findById("Element", self._svars.get('elementId')))
        notePosition = self.initPosition(note, BankNotePosition())
        notePosition.setCreditZpk(self.findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
        notePosition.setDebitZpk(self.findZpk(note.getPossession().getZpks(), 'POSSESSION'))
        return self.saveDocument(note)
    
    def remove(self):
        note = self.findById("BankNote", self._svars.get('id'))
        self.cancelNote(note)
        
        