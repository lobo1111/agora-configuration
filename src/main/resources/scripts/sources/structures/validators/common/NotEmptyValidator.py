from structures.validators.common.Validator import Validator

class NotEmptyValidator(Validator):
    
    def isValid(self, attribute):
        return attribute != None and attribute != ""