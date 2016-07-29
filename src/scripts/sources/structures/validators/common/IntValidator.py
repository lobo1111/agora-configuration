from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class IntValidator(Validator):
    _message = "validators.notInteger"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        try:
            value = int(attribute)
            self._logger.info("Validation passed:")
            self._logger.info("attribute - %s" % (self._messageParameter))
            self._logger.info("value - %s" % (str(attribute)))
            return value
        except:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        