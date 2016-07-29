from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class NotNoneValidator(Validator):
    _message = "validators.notNone"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        if attribute == None:
            raise ValidationError(self._label.get(self._message) % self._messageParameter)