from pl.reaper.container.data import InternalPayment
from java.util import Date
from base.Container import Container

class InternalPaymentManager(Container):
    
    def create(self):
        self._logger.info("Creating payment...")
        payment = InternalPayment()
        payment.setBookingPeriod(self.findDefaultBookingPeriod())
        payment.setCreatedDate(Date())
        payment.setBookedDate(None)
        payment.setCreditZpk(self.findZpkById(vars.get('creditZpkId')))
        self._logger.info("Credit zpk number - %s-%s" % (payment.getCreditZpk().getType().getKey(), payment.getCreditZpk().getNumber()))
        payment.setDebitZpk(self.findZpkById(vars.get('debitZpkId')))
        self._logger.info("Debit zpk number - %s-%s" % (payment.getDebitZpk().getType().getKey(), payment.getDebitZpk().getNumber()))
        payment.setBooked(False)
        payment.setAmount(float(vars.get('amount')))
        self._logger.info("Amount - %s" % (payment.getAmount()))
        payment.setComment(vars.get('comment'))
        entityManager.persist(payment)
        self._logger.info("Payment created")
        return payment
    
    def book(self):
        payment = self.findPaymentById(vars.get('paymentId'))
        if not payment.isBooked():
            self.increaseDebit(self.getCurrentBalance(payment.getDebitZpk()), payment.getAmount())
            self.increaseCredit(self.getCurrentBalance(payment.getCreditZpk()), payment.getAmount())
            payment.setBookedDate(Date())
            payment.setBooked(True)
            entityManager.persist(payment)
    
    def canCancel(self):
        payment = self.findPaymentById(vars.get('paymentId'))
        return not payment.isBooked()
    
    def cancel(self):
        if self.canCancel():
            payment = self.findPaymentById(vars.get('paymentId'))
            entityManager.remove(payment)
    
    def findDefaultBookingPeriod(self):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
    def findZpkById(self, id):
        return entityManager.createQuery('Select zpk From ZakladowyPlanKont zpk Where zpk.id = %s' % id).getSingleResult()
    
    def findPaymentById(self, id):
        return entityManager.createQuery('Select payment From InternalPayment payment Where payment.id = %s' % id).getSingleResult()
    
    def increaseDebit(self, balance, amount):
        balance.setDebit(balance.getDebit() + amount)
    
    def increaseCredit(self, balance, amount):
        balance.setCredit(balance.getCredit() + amount)
        
    def getCurrentBalance(self, zpk):
        currentBookingPeriod = self.findDefaultBookingPeriod()
        for balance in zpk.getZpkBalances():
            if balance.getBookingPeriod().equals(currentBookingPeriod):
                return balance
        return None