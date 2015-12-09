from actions.AbstractDocumentManager import AbstractDocumentManager

class PaymentRepairFundDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, payment):
        possession = payment.getPossession()
        account = self.getAccount(payment)
        zpkCredit = self.findZpk(possession.getZpks(), 'POSSESSION_REPAIR_FUND')
        zpkDebit = self.findZpk(account.getZpks(), 'REPAIR_FUND')
        return zpkCredit, zpkDebit
        
    def getAccount(self, payment):
        account = payment.getPaymentRentDetails().getAccount()
        if account.getType().getKey() == 'INDIVIDUAL':
            return account.getParrentAccount()
        else:
            return account