from documents.validators.Validator import Validator
from structures.validators.common.NotNoneValidator import NotNoneValidator
from structures.validators.common.DecimalValidator import DecimalValidator

class BankNoteValidator(Validator):
    
    def validate(self, document):
        self.check(document.getPossession(), [NotNoneValidator(messageParameter = self._label.get('validators.rentNote.possession'))])
        self.check(document.getPositions().get(0).getAttribute("ELEMENT_ID"), [NotNoneValidator(messageParameter = self._label.get('validators.rentNote.element'))])
        self.check(document.getPositions().get(0).getValue().floatValue(), [DecimalValidator(messageParameter = self._label.get('validators.rentNote.value'))])
        
    