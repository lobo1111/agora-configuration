from pl.reaper.container.data import Payment

class Payment(Container):
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def create(self):
        payment = Payment()
        print dir(payment)
        payment.setIncome(self.getIncome())
        payment.setType(self.getPaymentType())
        payment.setStatus(self.getPaymentStatus())
        payment.setAuto(0)
        payment.setPossession(self.getPossession())
        entityManager.persist(payment)
        
    def getPossession(self):
        sql = "Select possession From Possession possession Where possession.id = %d" % vars.get('possession')
        return entityManager.createQuery(sql).getSingleResult()
    
    def getIncome(self):
        return vars.get('income')
    
    def getPaymentType(self):
        return self._dictManager.getDictionaryInstance('PAYMENT_TYPE', vars.get('type'))
    
    def getPaymentStatus(self):
        return self._dictManager.getDictionaryInstance('PAYMENT_STATUS', 'NEW')