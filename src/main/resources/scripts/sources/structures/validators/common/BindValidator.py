from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class BindValidator(Validator):
    _message = "validators.common.bindNotFound"
    
    def __init__(self, entity, messageParameter = ''):
        self._entity = entity
        self._messageParameter = messageParameter
    
    def validate(self, value):
        entity = self.findById(self._entity, int(value))
        if entity == None:
            raise ValidationError(self._label.get(self._message) % self._messageParameter)
        else:
            return entity