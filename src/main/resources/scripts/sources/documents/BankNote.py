from documents.Document import DocumentManager

class BankNoteManager(DocumentManager):
    _type = "BANK_NOTE"
    
    def create(self):
        note = self.initDocument(self._type)
        note.setPossession(self.findById("Possession", self._svars.get('possessionId')))
        note.addAttribute("ELEMENT_ID", self._svars.get('elementId'))
        notePosition = self.initPosition(note)
        notePosition.setCreditZpk(self.findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
        notePosition.setDebitZpk(self.findZpk(note.getPossession().getZpks(), 'POSSESSION'))
        return self.saveDocument(note)
    
    def remove(self):
        note = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(note)
        
        