from pl.reaper.container.data import InternalPayment
from java.util import Date

class InternalPaymentManager:
    def create(self):
        payment = InternalPayment()
        payment.setBookingPeriod(self.findDefaultBookingPeriod())
        payment.setCreatedDate(Date())
        payment.setBookedDate(None)
        payment.setCreditZpk(self.findZpkById(vars.get('creditZpkId')))
        payment.setDebitZpk(self.findZpkById(vars.get('debitZpkId')))
        payment.setBooked(False)
        payment.setAmount(float(vars.get('amount')))
        payment.setComment(vars.get('comment'))
        entityManager.persist(payment)
        return payment
    
    def book(self):
        payment = self.findPaymentById(vars.get('paymentId'))
        if not payment.isBooked():
            self.increaseDebit(self.getCurrentBalance(payment.getDebitZpk()), payment.getAmount())
            self.increaseCredit(self.getCurrentBalance(payment.getCreditZpk()), payment.getAmount())
            self.setBookedDate(Date())
            self.setBooked(True)
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