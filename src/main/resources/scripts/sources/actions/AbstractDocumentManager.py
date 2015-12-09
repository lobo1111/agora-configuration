from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class AbstractDocumentManager(Container):
    
    def createDocument(self, entity, value, comment):
        zpkCredit, zpkDebit = self.collectZpks(entity)
        self._svars.put('creditZpkId', str(zpkCredit.getId()))
        self._svars.put('debitZpkId', str(zpkDebit.getId()))
        self._svars.put('amount', str(value))
        self._svars.put('comment', comment)
        manager = InternalPaymentManager()
        payment = manager.create()
        entity.setInternalPayment(payment)
        self.saveEntity(payment)
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))

    def findDebitZpk(self, zpks):
        return self.findZpk(zpks, 'CONTRACTOR')
    
    def findCreditZpk(self, community):
        return self.findZpk(community.getZpks(), 'RENT')
    
    def findZpk(self, zpks, typeKey):
        zpkType = self.findZpkType(typeKey)
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()