from pl.reaper.container.data import Payment
from java.math import BigDecimal
from java.util import Date

class PaymentManager(Container):
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def create(self):
        payment = Payment()
        payment.setIncome(self.getIncome())
        payment.setType(self.getPaymentType())
        payment.setStatus(self.getPaymentStatus())
        payment.setDescription(self.getDescription())
        payment.setCreateDay(Date())
        payment.setAccount(self.getAccount())
        if self.bookRequest():
            self.book(payment)
        entityManager.persist(payment)
        
    def bookStoredPayment(self):
        payment = self.findPaymentById(vars.get('id'))
        if not payment.getBooked() == False:
            self.book(payment)
        entityManager.persist(payment)
    
    def cancelStoredPayment(self):
        payment = self.findPaymentById(vars.get('id'))
        if not payment.getBooked() == True:
            BookingManager().unbook(payment)
        payment.setStatus(self.getPaymentCancelStatus())
        entityManager.persist(payment)
        
    def bookRequest(self):
        if vars.get('paymentBook') != None and vars.get('paymentBook') == 'true':
            return True
        else:
            return False
        
    def book(self, payment):
        BookingManager().book(payment)
        
    def getPossession(self):
        sql = "Select possession From Possession possession Where possession.id = %s" % vars.get('possession')
        return entityManager.createQuery(sql).getSingleResult()
    
    def getIncome(self):
        return BigDecimal(vars.get('paymentAmount'))
    
    def getDescription(self):
        return vars.get('paymentDescription')
    
    def getPaymentType(self):
        return self._dictManager.getDictionaryInstance(vars.get('paymentType'))
    
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'NEW_PAYMENT')
    
    def getAccount(self):
        return AccountManager().findAccountById(vars.get('accountId'))
    
    def findPaymentById(self, id):
        sql = "Select payment From Payment payment Where payment.id = %s" % id
        return entityManager.createQuery(sql).getSingleResult()
    
    def getPaymentCancelStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'CANCELED')