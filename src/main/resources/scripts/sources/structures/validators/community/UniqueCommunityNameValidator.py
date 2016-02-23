from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class UniqueCommunityNameValidator(Validator):
    _message = "validators.community.notUniqueName"
    
    def validate(self, attribute):
        communities = self.findAllBy("Community", "name", "'%s'" % attribute)
        for community in communities:
            if community != None and community.getOutDate() == None:
                raise ValidationError(self._label.get(self._message))
        