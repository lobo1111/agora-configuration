from structures.Dictionary import DictionaryManager
from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class DictionaryValidator(Validator):
    _message = "validators.dictionaryNotFound"
    
    def __init__(self, dictionary = "", messageParameter = ""):
        self._dictionary = dictionary
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        try:
            dict = DictionaryManager().findByValue(self._dictionary, attribute)
            self._logger.info("Validation passed:")
            self._logger.info("attribute - %s" % (self._messageParameter))
            return dict
        except:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        