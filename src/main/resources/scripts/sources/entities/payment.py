from pl.reaper.container.data import Payment
from pl.reaper.container.data.Payment import Direction
from java.math import BigDecimal
from java.util import Date

class PaymentManager(Container):
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def create(self):
        payment = Payment()
        self.setData(payment)
        entityManager.persist(payment)
        return payment
        
    def setData(self, payment):
        payment.setIncome(self.getIncome())
        payment.setType(self.getPaymentType())
        payment.setStatus(self.getPaymentStatus())
        payment.setDescription(self.getDescription())
        payment.setCreateDay(Date())
        if vars.get('paymentDirection') == 'INCOME':
            payment.setAccount(self.getAccount())
        payment.setDirection(self.getDirection())
        if self.bookRequest():
            self.book(payment)
        if vars.get('paymentCompanyId') != "0":
            payment.setCompany(CompanyManager().findCompanyById(vars.get('paymentCompanyId')))
        if vars.get('paymentPossessionId') != "0":
            payment.setPossession(PossessionManager().findPossessionById(vars.get('paymentPossessionId')))
        payment.setPossession(CommunityManager().findCommunityById(vars.get('paymentCommunityId')))
        
    def bookStoredPayment(self):
        payment = self.findPaymentById(vars.get('id'))
        if not payment.isBooked():
            self.book(payment)
        entityManager.persist(payment)
    
    def cancelStoredPayment(self):
        payment = self.findPaymentById(vars.get('id'))
        if payment.isBooked():
            BookingManager().unbook(payment)
        payment.setStatus(self.getPaymentCancelStatus())
        payment.setCancelComment(vars.get('paymentCancelComment'))
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
    
    def getDirection(self):
        if vars.get('paymentDirection') == 'INCOME':
            return Direction.INCOME
        if vars.get('paymentDirection') == 'EXPENDITURE':
            return Direction.EXPENDITURE
    
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'NEW_PAYMENT')
    
    def getAccount(self):
        return AccountManager().findAccountById(vars.get('accountId'))
    
    def findPaymentById(self, id):
        sql = "Select payment From Payment payment Where payment.id = %s" % id
        return entityManager.createQuery(sql).getSingleResult()
    
    def getPaymentCancelStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'CANCELED')