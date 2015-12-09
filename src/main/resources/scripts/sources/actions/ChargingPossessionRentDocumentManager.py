from actions.AbstractDocumentManager import AbstractDocumentManager

class ChargingPossessionRentDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, charge):
        possession = charge.getPossession()
        zpkDebit = self.getZpkRent(possession.getZpks())
        zpkCredit = self.findRentCreditZpk(possession.getCommunity())
        return zpkCredit, zpkDebit
    