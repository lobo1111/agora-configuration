from actions.AbstractDocumentManager import AbstractDocumentManager

class BankNoteDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, note):
        zpkCredit = self.findRentCreditZpk(note.getPossession().getCommunity())
        zpkDebit = self.getZpkRent(note.getPossession().getZpks())
        return zpkCredit, zpkDebit