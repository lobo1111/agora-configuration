from pl.reaper.container.data import BankCredit
from pl.reaper.container.data import BankCreditPayment
from base.Container import Container

class BankCreditManager(Container):

    def create(self):
        credit = BankCredit()
        credit.setCreatedAt(self.parseDate(self._svars.get("createdAt")))
        credit.setAmount(float(self._svars.get("amount")))
        credit.setCommunity(self.findById("Community", self._svars.get("communityId")))
        credit.setContractor(self.findById("Contractor", self._svars.get("contractorId")))
        for i in range(int(self._svars.get('paymentsCount'))): 
            payment = BankCreditPayment()
            payment.setCreatedAt(self.parseDate(self._svars.get(str(i) + '_payments_' + 'createdAt')))
            payment.setAmount(float(self._svars.get(str(i) + '_payments_' + 'amount')))
            payment.setId(int(self._svars.get(str(i) + '_payments_' + 'paymentId')))
            if self._svars.get(str(i) + '_payments_' + 'remove') == 'true':
                if payment.getId() != 0:
                    self._entityManager.remove(payment)
                    credit.getPayments().remove(payment)
                else:
                    #Marked as to remove but not stored so nothing to do.
                    pass
            else:
                payment.getBankCredit(credit)
                credit.getPayments().add(payment)
        self.saveEntity(credit)

    def remove(self):
        credit = self.findById("BankCredit", self._svars.get('id'))
        if credit.getPayments().size() == 0:
            self._entityManager.remove(credit)
        
    def markAsPayed(self):
        credit = self.findById("BankCredit", self._svars.get('id'))
        credit.setPayed(True)
        self.saveEntity(credit)
    
