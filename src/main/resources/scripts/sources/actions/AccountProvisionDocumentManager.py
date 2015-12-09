from actions.AbstractDocumentManager import AbstractDocumentManager

class AccountProvisionDocumentManager(AbstractDocumentManager):
 
    def collectZpks(self, provision):
        zpkCredit = self.findCreditZpk(provision.getAccount().getCommunity())
        zpkDebit = self.findDebitZpk(provision.getAccount().getBankContractor().getZpks())
        return zpkCredit, zpkDebit
