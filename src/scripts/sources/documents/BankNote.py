from documents.Document import DocumentManager

class BankNoteManager(DocumentManager):
    _type = "BANK_NOTE"
    
    def persist(self):
        return self.create()
    
    def create(self):
        note = self.initDocument(self._type)
        element = self.findById("Element", self._svars.get('elementId'))
        notePosition = self.initPosition(note)
        notePosition.putAttribute("ELEMENT_GROUP", element.getGroup().getValue())
        notePosition.putAttribute("ELEMENT_NAME", element.getName())
        notePosition.putAttribute("ELEMENT_ID", str(element.getId()))
        notePosition.setCreditZpk(self.findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
        notePosition.setDebitZpk(self.findZpk(note.getPossession().getZpks(), 'POSSESSION'))
        self.bound(note, notePosition)
        return self.saveDocument(note)
    
    def cancel(self):
        note = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(note)
        
        