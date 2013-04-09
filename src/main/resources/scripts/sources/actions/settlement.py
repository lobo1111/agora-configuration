class SettleManager(Container):
    _logger = Logger([:_scriptId])
    
    def settle(self):
        groupManager = self.findObligationGroup()
        balance = self.calculateBalance(groupManager)
        for zpk in groupManager.getZpks():
            amount = (zpk.getPossession().getShare().floatValue() / 100.0) * balance
            self.createPayment(zpk, amount)
            
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
    
    def createPayment(self, zpk, amount):
        self._logger.info("Creating expenditure(%f) for %s" % (amount, zpk.getNumber()))
        
    def findObligationGroup(self):
        return ObligationGroupManager().findObligationGroupById(vars.get('obligationGroupId'))
    
    def getDebit(self, zpk):
        for balance in zpk.getZpkBalances():
            if balance.getBookingPeriod().isDefaultPeriod():
                return balance.getDebit().floatValue()
        return 0.0;