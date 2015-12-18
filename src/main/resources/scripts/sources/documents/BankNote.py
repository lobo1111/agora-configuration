from documents.Document import DocumentManager

class BankNoteManager(DocumentManager):
    _type = "BANK_NOTE"
    
    def create(self):
        note = self.initDocument(self._type)
        notePosition = self.initPosition(note)
        notePosition.putAttribute("ELEMENT_GROUP", self._svars.get('elementGroup'))
        notePosition.setCreditZpk(self.findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
        notePosition.setDebitZpk(self.findZpk(note.getPossession().getZpks(), 'POSSESSION'))
        self.bound(note, notePosition)
        return self.saveDocument(note)
    
    def remove(self):
        note = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(note)
        
        