from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class UniqueInvoiceNumber(Validator):
    _message = "validators.invoice.number"
    
    def __init__(self, document):
        self._documentToCheck = document
    
    def validate(self, attribute):
        attributes = self.findAllBy("DocumentAttribute", "value", "'%s'" % attribute)
        for attribute in attributes:
            document = attribute.getDocument()
            if document.getType() == 'INVOICE' and attribute.getKey() == "NUMBER" and document.getId() != self._documentToCheck.getId() and document.getContractor().getId() == self._documentToCheck.getContractor().getId():
                raise ValidationError(self._label.get(self._message))
                