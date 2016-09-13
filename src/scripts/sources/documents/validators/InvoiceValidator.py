from documents.validators.Validator import Validator
from structures.validators.common.LengthValidator import LengthValidator

class InvoiceValidator(Validator):
    
    def validate(self, document):
        if not self.isAccepted(document):
            self.validateAttributes(document)
            self.validatePositions(document)
        self.validatePayments(document)
        
    def isAccepted(self, document):
        return document.getAttribute("ACCEPTED").getValue() == 'true'
        
    def validateAttributes(self, document):
        #self.check(document.getAttribute("NUMBER").getValue(), [LengthValidator(minLength = 1, maxLength = 250, messageParameter = self._label.get('field.invoiceNumber')), UniqueInvoiceNumber(currentId = document.getId())])
        self.check(document.getAttribute("NUMBER").getValue(), [LengthValidator(minLength = 1, maxLength = 250, messageParameter = self._label.get('field.companyName'))])
        self.check(document.getContractor(), [NotNoneValidator()])
        self.check(document.getAttribute("CREATE_DATE").getValue(), [NotNoneValidator()])
        self.check(document.getAttribute("PAYMENT_DATE").getValue(), [NotNoneValidator()])
    
    def validatePositions(self, document):
        for position in document.getPositions():
            if position.getType() == "INVOICE_COST":
                self.validatePosition(position)
            
    def validatePosition(self, position):
        pass
    
    def validatePayments(self, document):
        for position in document.getPositions():
            if position.getType() == "INVOICE_PAYMENT":
                self.validatePayment(position)
                
    def validatePayment(self, payment):
        pass