from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class DecimalValidator(Validator):
    _message = "validators.community.notUniqueName"
    
    def validate(self, attribute):
        community = self.findBy("Community", "name", "'%s'" % attribute)
        if community != None and community.getOutDate() == None:
            raise ValidationError(self._label.get(self._message))
        