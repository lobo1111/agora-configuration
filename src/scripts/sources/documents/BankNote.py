from documents.Document import DocumentManager
from documents.validators.BankNoteValidator import BankNoteValidator
from structures.validators.common.ValidationError import ValidationError

class BankNoteManager(DocumentManager):
    _type = "BANK_NOTE"
    
    def persist(self):
        try:
            return self.create()
        except ValidationError, error:
            self.setError(error)
    
    def create(self):
        note = self.initDocument(self._type)
        notePosition = self.initPosition(note)
        element = self.findById("Element", self._svars.get('elementId'))
        if element != None:
            notePosition.putAttribute("ELEMENT_GROUP", element.getGroup().getValue())
            notePosition.putAttribute("ELEMENT_NAME", element.getName())
            notePosition.putAttribute("ELEMENT_ID", str(element.getId()))
        notePosition.setCreditZpk(self.findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
        if note.getPossession() != None:
            notePosition.setDebitZpk(self.findZpk(note.getPossession().getZpks(), 'POSSESSION'))
        self.bound(note, notePosition)
        BankNoteValidator().validate(note)
        return self.saveDocument(note)
    
    def cancel(self):
        note = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(note)
        
        