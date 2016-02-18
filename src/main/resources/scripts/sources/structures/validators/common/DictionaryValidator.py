from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class DictionaryValidator(Validator):
    _message = "validators.dictionaryNotFound"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        if attribute == None:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        self._logger.info("Validation passed:")
        self._logger.info("attribute - %s" % (self._messageParameter))
        