class ChargingBooker:
    _logger = Logger([:_scriptId])
    
    def bookAllChargings(self):
        chargings = self.collectChargings()
        self._logger.info("Collected %d chargings to book" % chargings.size())
        for charge in chargings:
            self.bookCharging(charge)
            
    def collectChargings(self):
        return entityManager.createQuery('Select c From Charging c Join c.bookingPeriod p Where c.month In (SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT") and p.defaultPeriod = True').getResultList()
    
    def bookCharging(self, charge):
        possession = charge.getPossession()
        zpkRent = self.getZpkRent(possession.getZpks())
        zpkRepairFund = self.getZpkRepairFund(possession.getZpks())
        rentAmount = self.calculateRent(charge.getChargingElements())
        repairFundAmount = self.calculateRepairFund(charge.getChargingElements())
        self.bookAmount(self.findRentCreditZpk(possession.getCommunity()), zpkRent, rentAmount)
        self.bookAmount(self.findRepairFundCreditZpk(possession.getCommunity()), zpkRepairFund, repairFundAmount)
        
    def getZpkRent(self, zpks):
        for zpk in zpks:
            if zpk.getType().getKey() == "DEFAULT":
                return zpk
    
    def getZpkRepairFund(self, zpks):
        for zpk in zpks:
            if zpk.getType().getKey() == "REPAIR_FUND":
                return zpk
    
    def calculateRent(self, elements):
        value = 0.0
        for element in elements:
            if not element.getKey().startswith("R"):
                value += element.getValue()
        return value
    
    def calculateRepairFund(self, elements):
        value = 0.0
        for element in elements:
            if not element.getKey().startswith("R"):
                value += element.getValue()
        return value
    
    def bookAmount(self, creditZpk, zpk, amount):
        balance = self.getCurrentBalance(zpk)
        balance.setDebit(balance.getDebit() + amount)
        creditBalance = self.getCurrentBalance(creditZpk)
        creditBalance.setCredit(creditBalance.getCredit() + amount)
        entityManager.persist(balance)
        entityManager.persist(creditBalance)
        
    def getCurrentBalance(self, zpk):
        for balance in zpk.getZpkBalances():
            if balance.getBookingPeriod().isDefaultPeriod():
                return balance
    
    def findRentCreditZpk(self, community):
        type = self.findRentType()
        for zpk in community.getZpks():
            if zpk.getType().getKey() == type.getKey():
                return zpk
    
    def findRepairFundCreditZpk(self, community):
        type = self.findRepairFundType()
        for zpk in community.getZpks():
            if zpk.getType().getKey() == type.getKey():
                return zpk
            
    def findRentType(self):
        return entityManager.createQuery("Select d From	Dictionary d Where d.id IN (Select d.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = 'CHARGING_RENT')").getSingleResult()
    
    def findRepairFundType(self):
        return entityManager.createQuery("Select d From	Dictionary d Where d.id IN (Select d.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = 'CHARGING_REPAIR_FUND')").getSingleResult()
   
    
    
    