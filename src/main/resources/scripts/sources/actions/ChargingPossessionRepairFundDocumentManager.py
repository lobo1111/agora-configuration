from actions.AbstractDocumentManager import AbstractDocumentManager

class ChargingPossessionRepairFundDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, charge):
        possession = charge.getPossession()
        zpkDebit = self.getZpkRepairFund(possession.getZpks())
        zpkCredit = self.findRepairFundCreditZpk(possession.getCommunity())
        return zpkCredit, zpkDebit
    