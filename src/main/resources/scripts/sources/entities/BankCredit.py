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
        credit.setAccount(self.findById("Account", self._svars.get("accountId")))
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
        
    def switchAccounts(self, oldAccount, newAccount):
        self._logger.info("Switching accounts on credits from %d to %d" % (oldAccount.getId(), newAccount.getId()))
        credits = self._entityManager.createQuery('Select c From BankCredit c Where c.account.id = %d' % oldAccount.getId()).getResultList()
        self._logger.info("Found %d credits to change" % len(credits))
        for credit in credits:
            self._logger.info("Changing account on credit %d" % credit.getId())
            credit.setAccount(newAccount)
            self._entityManager.persist(credit)
            self._entityManager.flush()
        
    def updatePayments(self, credit):
        for i in range(int(self._svars.get('paymentsCount'))): 
            id = int(self._svars.get(str(i) + '_payments_' + 'paymentId'))
            remove = self._svars.get(str(i) + '_payments_' + 'remove') == 'true'
            payment = self.findOrCreatePayment(credit, id)
            payment.setCreatedAt(self.parseDate(self._svars.get(str(i) + '_payments_' + 'createdAt')))
            payment.setAmount(float(self._svars.get(str(i) + '_payments_' + 'amount')))
            if remove:
                self.removePayment(credit, payment)
            
    def findOrCreatePayment(self, credit, id):
        if id == 0:
            payment = BankCreditPayment()
            payment.setBankCredit(credit)
            credit.getPayments().add(payment)
            self._entityManager.persist(payment)
        else:
            payment = self.findById("BankCreditPayment", id);
        return payment
    
    def removePayment(self, credit, payment):
        credit.getPayments().remove(payment)
        self._entityManager.remove(payment)