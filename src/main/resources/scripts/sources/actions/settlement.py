class SettleManager(Container):
    _logger = Logger([:_scriptId])

    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def settle(self):
        groupManager = self.findObligationGroup()
        balance = self.calculateBalance(groupManager)
        log = self.addLog(groupManager, balance)
        self._logger.info("Balance calculated as %f" % balance)
        for zpk in groupManager.getZpks():
            share = (zpk.getPossession().getShare().floatValue() / 100.0)
            amount = self.round(share * balance)
            self._logger.info("Share calculated as %f" % share)
            self.createPayment(log, zpk, amount, groupManager.getCommunity().getId(), zpk.getPossession().getId())
        entityManager.persist(log) 
            
    def addLog(self, groupManager, balance):
        log = SettlementLog()
        log.setObligationGroup(groupManager)
        log.setCommunity(groupManager.getCommunity)
        log.setTotalIncome(self.calculateIncome(groupManager.getZpks()))
        log.setTotalObligations(self.calculateExpenditure(groupManager.getObligations()))
        log.setSettlementBalance(balance)
        log.setTotalArea(self.calculateTotalArea(groupManager.getZpks()))
        log.setReferenceRate(self.round(log.getTotalObligations() / log.getTotalArea()))
        return log
        
    def calculateTotalArea(self, zpks):
        total = 0.0
        for zpk in zpks:
            total += zpk.getPossession().getArea().floatValue()
        return total
            
    def calculateBalance(self, groupManager):
        income = self.calculateIncome(groupManager.getZpks())
        expenditure = self.calculateExpenditure(groupManager.getObligations())
        return (income - expenditure) * -1
    
    def calculateIncome(self, zpks):
        income = 0.0
        for zpk in zpks:
            income += self.getDebit(zpk)
        return income
    
    def calculateExpenditure(self, obligations):
        expenditure = 0.0
        for obligation in obligations:
            expenditure += self.getDebit(obligation.getZpk())
        return expenditure
    
    def createPayment(self, log, zpk, amount, communityId, possessionId):
        self._logger.info("Creating expenditure(%f) for %s" % (amount, zpk.getNumber()))
        vars.put('paymentPossessionId', str(possessionId))
        vars.put('paymentObligationId', str(0))
        vars.put('paymentCommunityId', str(communityId))
        vars.put('paymentBook', 'true')
        vars.put('paymentAmount', str(amount))
        vars.put('paymentDescription', 'Rozliczenie')
        vars.put('paymentType', self.getPaymentType().getId())
        vars.put('paymentDirection', 'EXPENDITURE')
        vars.put('zpkId', str(zpk.getId()))
        vars.put('paymentBookingPeriod', str(self.getDefaultPeriod(zpk).getId()))
        payment = PaymentManager().create()
        log.getPayments().add(payment)
        
    def findObligationGroup(self):
        return ObligationGroupManager().findObligationGroupById(vars.get('obligationGroupId'))
    
    def getDebit(self, zpk):
        for balance in zpk.getZpkBalances():
            if balance.getBookingPeriod().isDefaultPeriod():
                return balance.getDebit()
        return 0.0;
    
    def getDefaultPeriod(self, zpk):
        for balance in zpk.getZpkBalances():
            if balance.getBookingPeriod().isDefaultPeriod():
                return balance.getBookingPeriod()
        return None
    
    def getPaymentType(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_TYPE', 'SETTLEMENT')
    
    def round(self, toRound):
        return round(toRound, 2)