from documents.validators.Validator import Validator
from documents.validators.UniqueInvoiceNumber import UniqueInvoiceNumber
from structures.validators.common.LengthValidator import LengthValidator
from structures.validators.common.NotNoneValidator import NotNoneValidator
from structures.validators.common.DateValidator import DateValidator
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.IntValidator import IntValidator
from structures.validators.common.PositiveIntValidator import PositiveIntValidator
from helpers.Label import LabelManager

class InvoiceValidator(Validator):
    
    def validate(self, document):
        if not self.isAccepted(document):
            self.validateAttributes(document)
            self.validatePositions(document)
        self.validatePayments(document)
        
    def getNoZPKValidationError(self):
        return LabelManager().get('validators.invoice.noZPK')
        
    def isAccepted(self, document):
        return document.getAttribute("ACCEPTED").getValue() == 'true'
    
    def validateAttributes(self, document):
        self.check(document.getContractor(), [NotNoneValidator(messageParameter = self._label.get('validators.invoice.contractor'))])
        self.check(document.getAttribute("NUMBER").getValue(), [LengthValidator(minLength = 1, maxLength = 250, messageParameter = self._label.get('validators.invoice.number')), UniqueInvoiceNumber(document)])
        self.check(document.getAttribute("CREATE_DATE").getValue(), [DateValidator(messageParameter = self._label.get('validators.invoice.createDate'))])
        self.check(document.getAttribute("PAYMENT_DATE").getValue(), [DateValidator(messageParameter = self._label.get('validators.invoice.paymentDate'))])
    
    def validatePositions(self, document):
        for position in document.getPositions():
            if position.getType() == "INVOICE_COST":
                self.validatePosition(position)
            
    def validatePosition(self, position):
        self.check(position.getAttribute("NUMBER").getValue(), [IntValidator(messageParameter = self._label.get('validators.invoice.position.number'))])
        self.check(position.getAttribute("TAX_ID").getValue(), [PositiveIntValidator(messageParameter = self._label.get('validators.invoice.position.tax'))])
        self.check(position.getAttribute("VOLUME").getValue(), [DecimalValidator(messageParameter = self._label.get('validators.invoice.position.volume'))])
        self.check(position.getAttribute("VALUE_UNIT").getValue(), [DecimalValidator(messageParameter = self._label.get('validators.invoice.position.unitValueNet'))])
        self.check(position.getDescription(), [LengthValidator(minLength = 1, maxLength = 250, messageParameter = self._label.get('validators.invoice.position.name'))])
    
    def validatePayments(self, document):
        for position in document.getPositions():
            if position.getType() == "INVOICE_PAYMENT":
                self.validatePayment(position)
                
    def validatePayment(self, payment):
        self.check(payment.getAttribute("CREATE_DATE").getValue(), [DateValidator(messageParameter = self._label.get('validators.invoice.payment.paymentDate'))])
        self.check(payment.getAccount(), [NotNoneValidator(messageParameter = self._label.get('validators.invoice.payment.account'))])
        self.check(payment.getValue().floatValue(), [DecimalValidator(messageParameter = self._label.get('validators.invoice.payment.value'))])
        self.check(payment.getAttribute("COST_ID").getValue(), [PositiveIntValidator(messageParameter = self._label.get('validators.invoice.payment.costType'))])