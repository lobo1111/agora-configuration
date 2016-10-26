from documents.validators.UniqueInvoiceNumber import UniqueInvoiceNumber
from documents.validators.Validator import Validator
from helpers.Label import LabelManager
from structures.validators.common.DateValidator import DateValidator
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.IntValidator import IntValidator
from structures.validators.common.LengthValidator import LengthValidator
from structures.validators.common.NotNoneValidator import NotNoneValidator
from structures.validators.common.PositiveIntValidator import PositiveIntValidator

class InvoiceValidator(Validator):
    
    def validate(self, document):
        pass
        
    def validateAttributes(self, document):
        self.check(document.getContractor(), [NotNoneValidator(messageParameter = self._label.get('validators.invoice.contractor'))])
        self.check(document.getAttribute("NUMBER").getValue(), [LengthValidator(minLength = 1, maxLength = 250, messageParameter = self._label.get('validators.invoice.number')), UniqueInvoiceNumber(document)])
        self.check(document.getAttribute("CREATE_DATE").getValue(), [DateValidator(messageParameter = self._label.get('validators.invoice.createDate'))])
        self.check(document.getAttribute("PAYMENT_DATE").getValue(), [DateValidator(messageParameter = self._label.get('validators.invoice.paymentDate'))])
    