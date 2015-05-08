from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class PaymentBooker(Container):
    
    def bookAllPayments(self):
        self._logger.info("Payment Booker starts...")
        [self.bookPayment(payment) for payment in self.collectPayments()]
        self._logger.info("All payments booked")
        
    def collectPayments(self):
        return self._entityManager.createQuery('Select c From PaymentRent c Join c.bookingPeriod p Join c.possession possession Join possession.community community Where c.month In (SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT") and p.defaultPeriod = True and community.outDate is NULL').getResultList()
    
    def bookPayment(self, payment):
        self._logger.info("Booking payment %d" % payment.getId())
        possession = payment.getPossession()
        account = self.getAccount(payment)
        if payment.isRepairFund():
            zpkCreditAccount = self.findZpkPossessionRepairFund(possession.getZpks())
            zpkDebitAccount = self.findZpkCommunityRepairFundAccount(account.getZpks())
        else:
            zpkCreditAccount = self.findZpkPossessionRent(possession.getZpks())
            zpkDebitAccount = self.findZpkCommunityRentAccount(account.getZpks())
        self.createAndBookPayment(payment, zpkCreditAccount, zpkDebitAccount, payment.getPaymentRentDetails().getValue())

    def createAndBookPayment(self, rentPayment, creditZpk, debitZpk, amount):
        self._svars.put('creditZpkId', str(creditZpk.getId()))
        self._svars.put('debitZpkId', str(debitZpk.getId()))
        self._svars.put('amount', str(amount))
        self._svars.put('comment', 'Wplata')
        manager = InternalPaymentManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        payment = manager.create()
        rentPayment.setInternalPayment(payment)
        self.saveEntity(rentPayment)
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))
        manager.book()
        
    def findZpkPossessionRent(self, zpks):
        return self.findZpk(zpks, 'POSSESSION')
    
    def findZpkPossessionRepairFund(self, zpks):
        return self.findZpk(zpks, 'POSSESSION_REPAIR_FUND')
    
    def findZpkCommunityRentAccount(self, zpks):
        return self.findZpk(zpks, 'RENT', 'DEFAULT')
    
    def findZpkCommunityRepairFundAccount(self, zpks):
        return self.findZpk(zpks, 'REPAIR_FUND')
    
    def getAccount(self, payment):
        account = payment.getPaymentRentDetails().getAccount()
        if account.getType().getKey() == 'INDIVIDUAL':
            return account.getParrentAccount()
        else:
            return account
    
    def findZpk(self, zpks, typeKey, alternative = ''):
        zpkType = self.findZpkType(typeKey)
        self._logger.info('Looking for zpk type: %s' % typeKey)
        for zpk in zpks:
            self._logger.info('Checking: %s' % zpk.getType().getKey())
            if zpk.getType().getKey() == zpkType.getKey() or zpk.getType().getKey() == alternative:
                self._logger.info('Found it !')
                return zpk
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()
