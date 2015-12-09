from actions.AbstractDocumentManager import AbstractDocumentManager

class InvoiceCostDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, invoice):
        zpkCredit = self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR')
        zpkDebit = self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR_COST')
        return zpkCredit, zpkDebit