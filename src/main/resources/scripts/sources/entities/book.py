from java.lang import Double

class BookingManager(Container):
    
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def book(self, payment):
        payment.setStatus(self.getPaymentStatus())
        payment.setBooked(True)
        payment.setBookingDay(Date())
        bookingPeriod = self.getBookingPeriod()
        zpk = self.getZpk()
        print "!!!!!!!!!!" 
        print zpk
        balance = self.getZpkBalance(zpk, bookingPeriod)
        print "!!!!!"
        print balance
        balance.setDebit(balance.getDebit() + Double.parseDouble(vars.get('paymentAmount')))
        payment.setZpkBalance(balance)
        entityManager.persist(zpkBalance)
    
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'BOOKED')
    
    def getZpk(self):
        return ZpkManager().findZpkById(vars.get('zpkId'))
    
    def getZpkBalance(self, zpk, bookingPeriod):
        return ZpkManager().findBalanceByZpkAndPeriod(zpk, bookingPeriod)
        
    def getBookingPeriod(self):
        return BookingPeriodManager().findBookingPeriodById(vars.get('paymentBookingPeriod'))
        