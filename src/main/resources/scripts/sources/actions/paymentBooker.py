class PaymentBooker:
    _logger = Logger([:_scriptId])
    
    def bookAllPayments(self):
        self._logger.info("Payment Booker starts...")
        [self.bookPayment(payment) for payment in self.collectPayments()]
        self._logger.info("All payments booked")
        
    def collectPayments(self):
        return entityManager.createQuery('Select c From PaymentRent c Join c.bookingPeriod p Where c.month In (SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT") and p.defaultPeriod = True').getResultList()
    
    def bookPayment(self, payment):
        self._logger.info("Booking payment %d" % payment.getId())
        if self.isSimplePayment(payment):
            self.bookSimplePayment(payment)
        else:
            self.bookMultiPayment(payment)
                
    def bookSimplePayment(self, payment):
        possession = payment.getPossession()
        type = payment.getPaymentRentDetails().getAccount().getType().getKey()
        if type == 'RENT':
            zpkCreditAccount = self.findZpkPossessionRent(possession.getZpks())
        elif type == 'REPAIR_FUND':
            zpkCreditAccount = self.findZpkPossessionRepairFund(possession.getZpks())
        zpkDebitAccount = payment.getPaymentRentDetails().getAccount().getZpks().get(0)
        self.createAndBookPayment(zpkCreditAccount, zpkDebitAccount, payment.getPaymentRentDetails().getValue())
        
    def bookMultiPayment(self, payment):
        possession = payment.getPossession()
        zpkPossessionRent = self.findZpkPossessionRent(possession.getZpks())
        zpkPossessionRepairFund = self.findZpkPossessionRepairFund(possession.getZpks())
        zpkCommunityRentAccount = self.findZpkCommunityRentAccount(payment.getPaymentRentDetails().getAccount().getZpks())
        zpkCommunityRepairFundAccount = self.findZpkCommunityRepairFundAccount(payment.getPaymentRentDetails().getAccount().getZpks())
        amount = payment.getPaymentRentDetails().getValue()
        (rentAmount, repairFundAmount) = self.calculateAmounts(zpkPossessionRent, zpkPossessionRepairFund, amount)
        self.createAndBookPayment(zpkPossessionRent, zpkCommunityRentAccount, rentAmount)
        if repairFundAmount > 0:
            self.createAndBookPayment(zpkPossessionRepairFund, zpkCommunityRepairFundAccount, repairFundAmount)
        
    def createAndBookPayment(self, creditZpk, debitZpk, amount):
        vars.put('creditZpkId', str(creditZpk.getId()))
        vars.put('debitZpkId', str(debitZpk.getId()))
        vars.put('amount', str(amount))
        vars.put('comment', 'Wystawiono automatycznie')
        manager = InternalPaymentManager()
        payment = manager.create()
        entityManager.flush()
        vars.put('paymentId', str(payment.getId()))
        manager.book()
        
    def isSimplePayment(self, payment):
        return payment.getPaymentRentDetails().getAccount().getType().getKey() in ['RENT', 'REPAIR_FUND']
    
    def findZpkPossessionRent(self, zpks):
        return self.findZpk(zpks, 'POSSESSION')
    
    def findZpkPossessionRepairFund(self, zpks):
        return self.findZpk(zpks, 'POSSESSION_REPAIR_FUND')
    
    def findZpkCommunityRentAccount(self, zpks):
        return self.findZpk(zpks, 'RENT')
    
    def findZpkCommunityRepairFundAccount(self, zpks):
        return self.findZpk(zpks, 'REPAIR_FUND')
    
    def calculateAmounts(self, zpkPossessionRent, zpksPossessionRepairFund, amount):
        self._logger.info("Calculating amount %s" % str(amount))
        toPayOnRent = self.calculateToPay(zpkPossessionRent.getCurrentBalance().getCredit(), zpkPossessionRent.getCurrentBalance().getDebit())
        toPayOnRepairFund = self.calculateToPay(zpksPossessionRepairFund.getCurrentBalance().getCredit(), zpksPossessionRepairFund.getCurrentBalance().getDebit())
        self._logger.info("To pay on rent %s" % str(toPayOnRent))
        self._logger.info("To pay on repair fund %s" % str(toPayOnRepairFund))
        repairFundAmount = 0.0
        rentAmount = 0.0
        rentAmount = min(toPayOnRent, amount)
        amount -= min(toPayOnRent, amount)
        if amount >= toPayOnRepairFund:
            repairFundAmount = toPayOnRepairFund
            amount -= toPayOnRepairFund
        rentAmount += amount
        self._logger.info("Will pay on rent %s" % str(rentAmount))
        self._logger.info("Will pay on repair fund %s" % str(repairFundAmount))
        return rentAmount, repairFundAmount
    
    def calculateToPay(self, credit, debit):
        if credit >= debit:
            return 0.0
        else:
            return debit - credit
    
    def findZpk(self, zpks, typeKey):
        zpkType = self.findZpkType(typeKey)
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()