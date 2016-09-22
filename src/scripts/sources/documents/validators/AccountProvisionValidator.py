from documents.validators.Validator import Validator
from structures.validators.common.NotNoneValidator import NotNoneValidator
from structures.validators.common.DecimalValidator import DecimalValidator

class AccountProvisionValidator(Validator):
    
    def validate(self, document):
        self.check(document.getAccount(), [NotNoneValidator(messageParameter = self._label.get('field.accountNumber'))])
        self.check(document.getPositions().get(0).getValue().floatValue(), [DecimalValidator(messageParameter = self._label.get('field.value'))])
        
    