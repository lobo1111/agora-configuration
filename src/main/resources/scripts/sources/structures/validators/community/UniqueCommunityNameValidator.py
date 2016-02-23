from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class UniqueCommunityNameValidator(Validator):
    _message = "validators.community.notUniqueName"
    
    def validate(self, attribute):
        companies = self.findAllBy("Company", "name", "'%s'" % attribute)
        for company in companies:
            if company != None and companye.getCommunity().getOutDate() == None:
                raise ValidationError(self._label.get(self._message))
        