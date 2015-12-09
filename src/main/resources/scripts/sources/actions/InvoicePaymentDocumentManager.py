from actions.AbstractDocumentManager import AbstractDocumentManager

class InvoicePaymentDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, invoice):
        zpkCredit = self.findZpk(invoice.getCommunity().getZpks(), 'RENT')
        zpkDebit = self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR')
        return zpkCredit, zpkDebit