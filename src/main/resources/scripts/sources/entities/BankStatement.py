from base.Container import Container
from documents.Invoice import InvoiceManager
from documents.PaymentRent import PaymentRentManager

class BankStatementManager(Container):
    
    def create(self):
        invoiceType = self._svars.get('invoiceType') == 'true'
        if invoiceType:
            self.createInvoicePayment()
        else:
            self.createRentPayment()

    def createInvoicePayment(self):
        invoice = self.findById('Invoice', self._svars.get('invoiceId'))
        manager = InvoiceManager()
        manager.updatePayment(invoice)
        manager.saveDocument(invoice)

    def createRentPayment(self):
        PaymentRentManager().create()
