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
        zpkRentPossession = self.getZpkRent(possession.getZpks())
        zpkRepairFundPossession = self.getZpkRepairFund(possession.getZpks())
        rentAmount = self.calculateRent(charge.getChargingElements())
        repairFundAmount = self.calculateRepairFund(charge.getChargingElements())
        zpkRentCommunity = self.findRentCreditZpk(possession.getCommunity())
        zpkRepairFundCommunity = self.findRepairFundCreditZpk(possession.getCommunity())
        vars.set('creditZpkId', str(zpkRentCommunity.getId()))
        vars.set('debitZpkId', str(zpkRentPossession.getId()))
        vars.set('amount', str(rentAmount))
        vars.set('comment', 'Wystawiono automatycznie na podstawie naliczeń')
        manager = InternalPaymentManager()
        payment = manager.create()
        vars.set('paymentId', str(payment.getId()))
        manager.book()
        vars.set('creditZpkId', str(zpkRepairFundCommunity.getId()))
        vars.set('debitZpkId', str(zpkRepairFundPossession.getId()))
        vars.set('amount', str(repairFundAmount))
        vars.set('comment', 'Wystawiono automatycznie na podstawie naliczeń')
        manager = InternalPaymentManager()
        payment = manager.create()
        vars.set('paymentId', str(payment.getId()))
        manager.book()
        
    def calculateRent(self, elements):
        value = 0.0
        for element in elements:
            if not element.getKey().startswith("R"):
                value += element.getValue()
        return value
    
    def calculateRepairFund(self, elements):
        value = 0.0
        for element in elements:
            if element.getKey().startswith("R"):
                value += element.getValue()
        return value
        
    def getZpkRent(self, zpks):
        type = self.findRentTypePossession()
        for zpk in zpks:
            if zpk.getType().getKey() == type.getKey():
                return zpk
        self._logger.info("zpk rent not found !")
        self._logger.info(zpks)
    
    def getZpkRepairFund(self, zpks):
        type = self.findRepairFundTypePossession()
        for zpk in zpks:
            if zpk.getType().getKey() == type.getKey():
                return zpk
        self._logger.info("zpk repair fund not found !")
        self._logger.info(zpks)
    
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
        settings = str(entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = 'CHARGING_RENT'").getSingleResult())
        return entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % settings).getSingleResult()
    
    def findRentTypePossession(self):
        settings = str(entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = 'POSSESSION'").getSingleResult())
        return entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % settings).getSingleResult()
    
    def findRepairFundType(self):
        settings = str(entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = 'CHARGING_REPAIR_FUND'").getSingleResult())
        return entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % settings).getSingleResult()
   
    def findRepairFundTypePossession(self):
        settings = str(entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = 'POSSESSION_REPAIR_FUND'").getSingleResult())
        return entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % settings).getSingleResult()
    
    
    