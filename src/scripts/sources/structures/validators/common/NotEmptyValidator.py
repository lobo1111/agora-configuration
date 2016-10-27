from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class NotEmptyValidator(Validator):
    _message = "validators.notNone"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        if attribute == None or attribute == '':
            raise ValidationError(self._label.get(self._message) % self._messageParameter)