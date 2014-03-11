from pl.reaper.container.data import InternalPayment
from java.util import Date

class InternalPaymentManager:
    def create(self):
        payment = InternalPayment()
        payment.setBookingPeriod(self.findDefaultBookingPeriod())
        payment.setCreateDate(self.parseDate(vars.get('createDate')))
        payment.setBookedDate(None)
        payment.setCreditZpk(self.findZpkById(vars.get('creditZpkId')))
        payment.setDebitZpk(self.findZpkById(vars.get('creditZpkId')))
        payment.setBooked(False)
        payment.setCredit(float(vars.get('credit')))
        payment.setDebit(float(vars.get('debit')))
        payment.setComment(vars.get('comment'))
        entityManager.persist(payment)
        return payment
    
    def book(self):
        payment = self.findPaymentById(vars.get('paymentId'))
        if not payment.isBooked() == False:
            self.increaseDebit(self.getCurrentBalance(payment.getDebitZpk()), payment.getDebit())
            self.increaseCredit(self.getCurrentBalance(payment.getCreditZpk()), payment.getCredit())
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
    
    def parseDate(self, date):
        try:
            return SimpleDateFormat('dd-MM-yy').parse(date)
        except:
            return None
        
    def findDefaultBookingPeriod(self):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
    def findZpkById(self, id):
        return entityManager.createQuery('Select zpk From ZakładowyPlanKont zpk Where zpk.id = %s' % id).getSingleResult()
    
    def findPaymentById(self, id):
        return entityManager.createQuery('Select payment From InternalPayment payment Where payment.id = %s' % id).getSingleResult()
    
    def increaseDebit(self, balance, amount):
        balance.setDebit(balance.getDebit() + amount)
    
    def increaseCredit(self, balance, amount):
        balance.setCredit(balance.getCredit() + amount)
        
    def getCurrentBalance(self, zpk):
        currentBookingPeriod = self.findDefaultBookingPeriod()
        for balance in zpk.getZpkBalances():
            if balance.getBookingPeriod.equals(currentBookingPeriod):
                return balance
        return None