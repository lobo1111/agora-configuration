from structures.validators.common.Validator import Validator

class LengthValidator(Validator):
    _messageMin = "validators.lengthValidatorMin"
    _messageMax = "validators.lengthValidatorMax"
    _messageMinMax = "validators.lengthValidatorMinMax"
    
    def __init__(self, minLength = None, maxLength = None, messageParameter = ""):
        self._minLength = minLength
        self._maxLength = maxLength
        self._messageParameter = messageParameter
        
    def validate(self, attribute):
        if (self._minLength != None and len(attribute) < self._minLength) or (self._maxLength != None and len(attribute) > self._maxLength):
            if self._minLength == None and self._minLength != None:
                raise ValidationError(self._label.get(self._messageMax) % (self._messageParameter, self._maxLength))
            if self._minLength != None and self._minLength == None:
                raise ValidationError(self._label.get(self._messageMin) % (self._messageParameter, self._minLength))
            if self._minLength != None and self._minLength != None:
                raise ValidationError(self._label.get(self._messageMinMax) % (self._messageParameter, self._minLength, self._maxLength))
        self._logger.info("Validation passed:")
        self._logger.info("min: - %s, max - %s, attribute - %s" % (self._minLength, self._maxLength, self._messageParameter))
        