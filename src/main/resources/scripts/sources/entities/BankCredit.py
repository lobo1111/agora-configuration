from pl.reaper.container.data import BankCredit
from base.Container import Container

class BankCreditManager(Container):

    def create(self):
        credit = BankCredit()
        credit.setCreatedAt(self.parseDate(self._svars.get("createdAt")))
        credit.setAmount(float(self._svars.get("amount")))
        credit.setCommunity(self.findById("Community", self._svars.get("communityId")))
        credit.setContractor(self.findById("Contractor", self._svars.get("contratorId")))
        self.saveEntity(credit)

    def remove(self):
        pass
        #note = self.findById("BankNote", self._svars.get('id'))
        #if note.getInternalPayment() == None:
        #    self._entityManager.remove(note)
    
