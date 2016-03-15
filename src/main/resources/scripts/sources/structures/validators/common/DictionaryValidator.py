from base.Container import Container
from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class DictionaryValidator(Validator):
    _message = "validators.dictionaryNotFound"
    
    def __init__(self, dictionary = "", messageParameter = ""):
        self._dictionary = dictionary
        self._messageParameter = messageParameter
        
    def validate(self, attributeId):
        dict = Container().findById("Dictionary", attributeId)
        if dict != None and dict.getType().getType() == self._dictionary:
            self._logger.info("Validation passed:")
            self._logger.info("attribute - %s" % (self._messageParameter))
            return dict
        else:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))

        