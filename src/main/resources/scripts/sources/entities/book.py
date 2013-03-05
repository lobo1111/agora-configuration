from java.lang import Double

class BookingManager(Container):
    _logger = Logger([:_scriptId])
    
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def book(self, payment):
        payment.setStatus(self.getPaymentStatus())
        payment.setBooked(True)
        payment.setBookingDay(Date())
        zpk = self.getZpk()
        bookingPeriod = self.getBookingPeriod()
        balance = self.getZpkBalance(zpk, bookingPeriod)
        payment.setZpkBalance(balance)
        self._logger.info('Booking payment in period %s' % bookingPeriod.getName())
        self.bookInPeriod(bookingPeriod, payment)
        self._logger.info('Now booking in children...')
        self.bookInChildren(self.findChild(bookingPeriod), payment)
        self._logger.info('Booking complete.')
        
    def bookInChildren(self, bookingPeriod, payment):
        while bookingPeriod != None:
            self._logger.info('Booking in child period %s' % bookingPeriod.getName())
            self.updateStartBalance(bookingPeriod, payment, self.getZpk())
            self.bookInPeriod(bookingPeriod, payment)
            bookingPeriod = self.findChild(bookingPeriod)
            
    def findChild(self, bookingPeriod):
        return BookingPeriodManager().findChild(bookingPeriod)
    
    def updateStartBalance(self, bookingPeriod, payment, zpk):
        balance = self.getZpkBalance(zpk, bookingPeriod)
        if payment.getDirection().equals(Payment.Direction.INCOME):
            calculated = self.calculateAmount(balance.getStartCredit(), payment.getIncome().floatValue(), 1)
            balance.setStartCredit(calculated)
        elif payment.getDirection().equals(Payment.Direction.EXPENDITURE):
            calculated = self.calculateAmount(balance.getStartCredit(), payment.getIncome().floatValue(), -1)
            balance.setStartDebit(calculated)
        entityManager.persist(balance)
    
    def bookInPeriod(self, bookingPeriod, payment):
        zpk = self.getZpk()
        balance = self.getZpkBalance(zpk, bookingPeriod)
        self.setAmount(payment, balance, 1)
        entityManager.persist(balance)
    
    def unbook(self, payment):
        payment.setBooked(False)
        balance = payment.getZpkBalance()
        self.setAmount(payment, balance, -1)
        entityManager.persist(balance)
        self.unbookInChildren(self.findChild(balance.getBookingPeriod()), payment)
        
    def unbookInPeriod(self, bookingPeriod, payment):
        zpk = ZpkManager().findZpkById(payment.getZpk().getId())
        balance = self.getZpkBalance(zpk, bookingPeriod)
        self.setAmount(payment, balance, -1)
        payment.setZpkBalance(balance)
        entityManager.persist(balance)
        
    def unbookInChildren(self, bookingPeriod, payment):
         while bookingPeriod != None:
            self.updateStartBalance(bookingPeriod, payment, ZpkManager().findZpkById(payment.getZpkBalance().getZpk().getId()))
            self.unbookInPeriod(bookingPeriod, payment)
            bookingPeriod = self.findChild(bookingPeriod)
        
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
        