from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class DateValidator(Validator):
    _message = "validators.notDate"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        value = self.parseDate(attribute)
        if value != None:
            self._logger.info("Validation passed:")
            self._logger.info("attribute - %s" % (self._messageParameter))
            self._logger.info("value - %s" % (str(attribute)))
            return value
        else:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        