from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class PositiveIntValidator(Validator):
    _message = "validators.notInteger"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        try:
            value = int(attribute)
            if value > 0:
                self._logger.info("Validation passed:")
                self._logger.info("attribute - %s" % (self._messageParameter))
                self._logger.info("value - %s" % (str(attribute)))
                return value
            else:
                raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        except:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        