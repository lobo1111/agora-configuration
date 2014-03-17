class ChargingBooker:
    _logger = Logger([:_scriptId])
    
    def bookAllChargings(self):
        self._logger.info("Charging Booker starts...")
        [self.bookCharging(charge) for charge in self.collectChargings()]
        self._logger.info("All chargings booked")
            
    def collectChargings(self):
        return entityManager.createQuery('Select c From Charging c Join c.bookingPeriod p Where c.month In (SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT") and p.defaultPeriod = True').getResultList()
    
    def bookCharging(self, charge):
        self.createPaymentForRent(charge)
        self.createPaymentForRepairFund(charge)

    def createPaymentForRent(self, charge):
        possession = charge.getPossession()
        zpkRentPossession = self.getZpkRent(possession.getZpks())
        rentAmount = self.calculateRent(charge.getChargingElements())
        zpkRentCommunity = self.findRentCreditZpk(possession.getCommunity())
        self.createAndBookPayment(zpkRentCommunity, zpkRentPossession, rentAmount)
        
    def createPaymentForRepairFund(self, charge):
        possession = charge.getPossession()
        zpkRepairFundPossession = self.getZpkRepairFund(possession.getZpks())
        repairFundAmount = self.calculateRepairFund(charge.getChargingElements())
        zpkRepairFundCommunity = self.findRepairFundCreditZpk(possession.getCommunity())
        self.createAndBookPayment(zpkRepairFundCommunity, zpkRepairFundPossession, repairFundAmount)
        
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
        
    def calculateRent(self, elements):
        return self.calculate(elements, False)
    
    def calculateRepairFund(self, elements):
        return self.calculate(elements, True)
    
    def calculate(self, elements, repairFund):
        return [sum(element.getValue()) for element in elements if (element.getGroup().getKey() == 'REPAIR_FUND') == repairFund]
        
    def getZpkRent(self, zpks):
        return self.findCreditZpk(zpks, 'POSSESSION')
    
    def getZpkRepairFund(self, zpks):
        return self.findCreditZpk(zpks, 'POSSESSION_REPAIR_FUND')
    
    def findRentCreditZpk(self, community):
        return self.findCreditZpk(community.getZpks(), 'CHARGING_RENT')
    
    def findRepairFundCreditZpk(self, community):
        return self.findCreditZpk(community.getZpks(), 'CHARGING_REPAIR_FUND')
            
    def findCreditZpk(self, zpks, typeKey):
        return next(lambda zpk: zpk.getType().getKey() == self.findZpkType(typeKey).getKey(), zpks)
            
    def findZpkType(self, typeKey):
        return self.findZpkSettingId(typeKey)
    
    def findDictionary(self, id):
        return entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()