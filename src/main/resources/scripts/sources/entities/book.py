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
        self.setAmount(payment, balance, 1)
        payment.setZpkBalance(balance)
        entityManager.persist(balance)
    
    def unbook(self, payment):
        payment.setBooked(False)
        balance = payment.getZpkBalance()
        self.setAmount(payment, balance, -1)
        entityManager.persist(balance)
        
    def setAmount(self, payment, balance, book):
        if payment.getDirection().equals(Payment.Direction.INCOME):
            calculated = self.calculateAmount(balance.getCredit(), payment.getIncome().floatValue(), 1 * book)
            balance.setCredit(calculated)
        elif payment.getDirection().equals(Payment.Direction.EXPENDITURE):
            calculated = self.calculateAmount(balance.getDebit(), payment.getIncome().floatValue(), 1 * book)
            balance.setDebit(calculated)
            
    def calculateAmount(self, base, payment, factor):
        return base + (factor * payment)
    
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'BOOKED')
    
    def getZpk(self):
        return ZpkManager().findZpkById(vars.get('zpkId'))
    
    def getZpkBalance(self, zpk, bookingPeriod):
        return ZpkManager().findBalanceByZpkAndPeriod(zpk, bookingPeriod)
        
    def getBookingPeriod(self):
        return BookingPeriodManager().findBookingPeriodById(vars.get('paymentBookingPeriod'))
        