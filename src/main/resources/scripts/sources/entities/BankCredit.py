from base.Container import Container
from pl.reaper.container.data import BankCredit
from pl.reaper.container.data import BankCreditPayment

class BankCreditManager(Container):

    def create(self):
        credit = BankCredit()
        credit.setCreatedAt(self.parseDate(self._svars.get("createdAt")))
        credit.setAmount(float(self._svars.get("amount")))
        credit.setCommunity(self.findById("Community", self._svars.get("communityId")))
        credit.setContractor(self.findById("Contractor", self._svars.get("contractorId")))
        self.updatePayments(credit)
        self.saveEntity(credit)
        
    def update(self):
        credit = self.findById("BankCredit", self._svars.get('id'))
        self.updatePayments(credit)
        self.saveEntity(credit)

    def remove(self):
        credit = self.findById("BankCredit", self._svars.get('id'))
        if credit.getPayments().size() == 0:
            self._entityManager.remove(credit)
        
    def markAsPayed(self):
        credit = self.findById("BankCredit", self._svars.get('id'))
        credit.setPayed(True)
        self.saveEntity(credit)
        
    def updatePayments(self, credit):
        for i in range(int(self._svars.get('paymentsCount'))): 
            payment = BankCreditPayment()
            payment.setCreatedAt(self.parseDate(self._svars.get(str(i) + '_payments_' + 'createdAt')))
            payment.setAmount(float(self._svars.get(str(i) + '_payments_' + 'amount')))
            payment.setId(int(self._svars.get(str(i) + '_payments_' + 'paymentId')))
            if self._svars.get(str(i) + '_payments_' + 'remove') == 'true':
                if self._entityManager.containes(payment):
                    self._entityManager.remove(payment)
                    credit.getPayments().remove(payment)
                else:
                    #Marked as to remove but not stored so nothing to do.
                    payment = None
            else:
                payment.setBankCredit(credit)
                credit.getPayments().add(payment)
    
