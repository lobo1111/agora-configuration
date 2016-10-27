from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class PaymentOverpaymentValidator(Validator):
    
    def __init__(self):
        self._message = "validators.document.payment.overpayment"
    
    def validate(self):
        if float(self._svars.get('overpayedValue')) > 0 and int(self._svars.get('overpayedId')) <= 0:
            raise ValidationError(self._label.get(self._message))
                