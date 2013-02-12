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
        balance = self.getZpkBalance(zpk, bookingPeriod)
        balance.setDebit(balance.getDebit() + Double.parseDouble(vars.get('paymentAmount')))
        payment.setZpkBalance(balance)
        entityManager.persist(zpkBalance)
    
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'BOOKED')
    
    def getZpk(self):
        ZpkManager().findZpkById(vars.get('zpkId'))
    
    def getZpkBalance(self, zpk, bookingPeriod):
        ZpkManager().findBalanceByZpkAndPeriod(zpk, bookingPeriod)
        
    def getBookingPeriod(self):
        BookingPeriodManager().findBookingPeriodById(vars.get('paymentBookingPeriod'))
        