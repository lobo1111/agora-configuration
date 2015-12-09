from actions.AbstractDocumentManager import AbstractDocumentManager

class BankCreditDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, cPayment):
        zpkCredit = self.findCreditZpk(cPayment.getBankCredit().getContractor().getZpks())
        zpkDebit = self.findDebitZpk(cPayment.getBankCredit().getCommunity().getZpks(), cPayment.getBankCredit().isChargeDefaultAccount())
        return zpkCredit, zpkDebit