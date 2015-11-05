from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class BankCreditBooker(Container):
    
    def bookAllCredits(self):
        self._logger.info("Bank Credit Booker starts...")
        [self.bookCredit(cPayment) for cPayment in self.collectCredits()]
        self._logger.info("All bank credits booked")
        
    def collectCredits(self):
        return self._entityManager.createQuery('Select c From BankCreditPayment c Where c.internalPayment is null').getResultList()
    
    def bookCredit(self, cPayment):
        self._logger.info("Booking credit payment %d" % cPayment.getId())
        zpkCredit, zpkDebit = self.collectZpks(cPayment)
        self.createAndBookPayment(cPayment, zpkCredit, zpkDebit)

    def createAndBookPayment(self, cPayment, zpkCredit, zpkDebit):
        self._svars.put('creditZpkId', str(zpkCredit.getId()))
        self._svars.put('debitZpkId', str(zpkDebit.getId()))
        self._svars.put('amount', str(cPayment.getAmount()))
        self._svars.put('comment', 'Kredyt Bankowy')
        manager = InternalPaymentManager()
        payment = manager.create()
        cPayment.setInternalPayment(payment)
        self.saveEntity(payment)
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))
        manager.book()

    def collectZpks(self, cPayment):
        zpkCredit = self.findCreditZpk(cPayment.getBankCredit().getContractor().getZpks())
        zpkDebit = self.findDebitZpk(cPayment.getBankCredit().getCommunity().getZpks(), cPayment.getBankCredit().isChargeDefaultAccount())
        return zpkCredit, zpkDebit

    def findDebitZpk(self, zpks, chargeFromDefault):
        if chargeFromDefault:
            return self.findZpk(zpks, 'RENT')
        else:
            return self.findZpk(zpks, 'REPAIR_FUND')
    
    def findCreditZpk(self, zpks):
        return self.findZpk(zpks, 'CONTRACTOR')
    
    def findZpk(self, zpks, typeKey):
        zpkType = self.findZpkType(typeKey)
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()