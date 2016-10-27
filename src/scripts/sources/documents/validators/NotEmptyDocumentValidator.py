from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class NotEmptyDocumentValidator(Validator):
    
    def __init__(self):
        self._message = "validators.document.notEmpty"
    
    def validate(self, positions):
        if len(positions) == 0:
            raise ValidationError(self._label.get(self._message))
                