class SettleManager(Container):
    _logger = Logger([:_scriptId])

    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def settle(self):
        groupManager = self.findObligationGroup()
        balance = self.calculateBalance(groupManager)
        self._logger.info("Balance calculated as %f" % balance)
        for zpk in groupManager.getZpks():
            share = (zpk.getPossession().getShare().floatValue() / 100.0)
            amount = share * balance
            self._logger.info("Share calculated as %f" % share)
            self.createPayment(zpk, amount, groupManager.getCommunity().getId(), zpk.getPossession().getId())
            
    def calculateBalance(self, groupManager):
        income = self.calculateIncome(groupManager.getZpks())
        expenditure = self.calculateExpenditure(groupManager.getObligations())
        return income - expenditure
    
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
    
    def createPayment(self, zpk, amount, communityId, possessionId):
        self._logger.info("Creating expenditure(%f) for %s" % (amount, zpk.getNumber()))
        vars.put('paymentPossessionId', str(possessionId))
        vars.put('paymentCommunityId', str(communityId))
        vars.put('paymentBook', 'true')
        vars.put('paymentAmount', str(amount))
        vars.put('paymentDescription', 'Rozliczenie')
        vars.put('paymentType', self.getPaymentType().getId())
        vars.put('paymentDirection', 'EXPENDITURE')
        vars.put('zpkId', str(zpk.getId()))
        vars.put('paymentBookingPeriod', str(self.getDefaultPeriod(zpk).getId()))
        PaymentManager().create()
        
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
        return self._dictManager.getDictionaryInstance('SETTLEMENT')