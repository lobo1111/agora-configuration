from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class AccountProvisionBooker(Container):
    
    def bookAllProvisions(self):
        self._logger.info("Accont Provision Booker starts...")
        [self.bookProvision(provision) for provision in self.collectProvisions()]
        self._logger.info("All account provisions booked")
        
    def collectProvisions(self):
        return self._entityManager.createQuery('Select c From AccountProvision c Where c.internalPayment is null').getResultList()
    
    def bookProvision(self, provision):
        self._logger.info("Booking provision %d" % provision.getId())
        zpkCredit, zpkDebit = self.collectZpks(provision)
        self.createAndBookPayment(provision, zpkCredit, zpkDebit)

    def createAndBookPayment(self, provision, zpkCredit, zpkDebit):
        self._svars.put('creditZpkId', str(zpkCredit.getId()))
        self._svars.put('debitZpkId', str(zpkDebit.getId()))
        self._svars.put('amount', str(provision.getProvisionValue()))
        self._svars.put('comment', 'Prowizja')
        manager = InternalPaymentManager()
        payment = manager.create()
        provision.setInternalPayment(payment)
        self.saveEntity(payment)
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))
        manager.book()

    def collectZpks(self, provision):
        zpkCredit = self.findCreditZpk(provision.getAccount().getCommunity())
        zpkDebit = self.findDebitZpk(provision.getAccount().getBankContractor().getZpks())
        return zpkCredit, zpkDebit

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