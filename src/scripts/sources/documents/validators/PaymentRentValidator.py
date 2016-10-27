from documents.validators.Validator import Validator
from documents.validators.NotEmptyDocumentValidator import NotEmptyDocumentValidator
from structures.validators.common.DateValidator import DateValidator
from structures.validators.common.NotNoneValidator import NotNoneValidator

class PaymentRentValidator(Validator):
    
    def validate(self, document):
        self.check(document.getPossession(), [NotNoneValidator(messageParameter = self._label.get('field.possession'))])
        for position in document.getPositions():
            self.validatePosition(position)
        self.check(document.getPositions(), [NotEmptyDocumentValidator()])
        
    def validatePosition(self, position):
        self.check(position.getAccount(), [NotNoneValidator(messageParameter = self._label.get('field.account'))])
        self.check(position.getDescription(), [NotNoneValidator(messageParameter = self._label.get('field.description'))])
        self.check(position.getClientName(), [NotNoneValidator(messageParameter = self._label.get('field.clientName'))])
        self.check(position.getAttribute("CREATE_DATE").getValue(), [DateValidator(messageParameter = self._label.get('field.createDate'))])
        self.check(position.getAttribute("BOOKING_DATE").getValue(), [DateValidator(messageParameter = self._label.get('field.bookedDate'))])
        