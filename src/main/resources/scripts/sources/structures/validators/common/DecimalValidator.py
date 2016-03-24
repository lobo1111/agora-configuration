from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class DecimalValidator(Validator):
    _message = "validators.notDecimal"
    
    def __init__(self, messageParameter = ""):
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        try:
            value = float(attribute)
            self._logger.info("Validation passed:")
            self._logger.info("attribute - %s" % (self._messageParameter))
            self._logger.info("value - %s" % (str(attribute)))
            return value
        except:
            raise ValidationError(self._label.get(self._message) % (self._messageParameter))
        