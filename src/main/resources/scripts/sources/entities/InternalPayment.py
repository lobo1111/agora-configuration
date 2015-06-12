from pl.reaper.container.data import InternalPayment
from java.util import Date
from base.Container import Container

class InternalPaymentManager(Container):
    
    def create(self):
        payment = InternalPayment()
        payment.setBookingPeriod(self.findDefaultBookingPeriod())
        payment.setCreatedDate(Date())
        payment.setBookedDate(None)
        payment.setCreditZpk(self.findById('ZakladowyPlanKont', self._svars.get('creditZpkId')))
        payment.setDebitZpk(self.findById('ZakladowyPlanKont', self._svars.get('debitZpkId')))
        payment.setBooked(False)
        payment.setAmount(float(self._svars.get('amount')))
        payment.setComment(self._svars.get('comment'))
        self.saveEntity(payment)
        return payment
    
    def book(self):
        payment = self.findById('InternalPayment', self._svars.get('paymentId'))
        if not payment.isBooked():
            self.increaseDebit(self.getCurrentBalance(payment.getDebitZpk()), payment.getAmount())
            self.increaseCredit(self.getCurrentBalance(payment.getCreditZpk()), payment.getAmount())
            payment.setBookedDate(Date())
            payment.setBooked(True)
            self._entityManager.persist(payment)
    
    def canCancel(self):
        payment = self.findById('InternalPayment', self._svars.get('paymentId'))
        return not payment.isBooked()
    
    def cancel(self):
        if self.canCancel():
            payment = self.findById('InternalPayment', self._svars.get('paymentId'))
            self._entityManager.remove(payment)

    def cancelBookedPayment(self, internalPayment):
        debitBalance = internalPayment.getDebitZpk().getCurrentBalance()
        creditBalance = internalPayment.getCreditZpk().getCurrentBalance()
        self.increaseDebit(debitBalance, internalPayment.getAmount() * -1)
        self.increaseCredit(creditBalance, internalPayment.getAmount() * -1)
        self._entityManager.persist(debitBalance)
        self._entityManager.persist(creditBalance)
        self._entityManager.remove(internalPayment)
    
    def findDefaultBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
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