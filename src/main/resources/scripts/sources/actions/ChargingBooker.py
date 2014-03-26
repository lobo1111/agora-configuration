from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class ChargingBooker(Container):
    
    def bookAllChargings(self):
        self._logger.info("Charging Booker starts...")
        [self.bookCharging(charge) for charge in self.collectChargings()]
        self._logger.info("All chargings booked")
            
    def collectChargings(self):
        return self._entityManager.createQuery('Select c From Charging c Join c.bookingPeriod p Where c.month In (SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT") and p.defaultPeriod = True').getResultList()
    
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
        
        self._svars.put('creditZpkId', str(creditZpk.getId()))
        self._svars.put('debitZpkId', str(debitZpk.getId()))
        self._svars.put('amount', str(amount))
        self._svars.put('comment', 'Wystawiono automatycznie')
        manager = InternalPaymentManager()
        manager.setEntityManager(self._entityManager)
        payment = manager.create()
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))
        manager.book()
        
    def calculateRent(self, elements):
        return self.calculate(elements, False)
    
    def calculateRepairFund(self, elements):
        return self.calculate(elements, True)
    
    def calculate(self, elements, repairFund):
        return sum([element.getValue() for element in elements if (element.getGroup().getKey() == 'REPAIR_FUND') == repairFund])
        
    def getZpkRent(self, zpks):
        return self.findZpk(zpks, 'POSSESSION')
    
    def getZpkRepairFund(self, zpks):
        return self.findZpk(zpks, 'POSSESSION_REPAIR_FUND')
    
    def findRentCreditZpk(self, community):
        return self.findZpk(community.getZpks(), 'CHARGING_RENT')
    
    def findRepairFundCreditZpk(self, community):
        return self.findZpk(community.getZpks(), 'CHARGING_REPAIR_FUND')
            
    def findZpk(self, zpks, typeKey):
        zpkType = self.findZpkType(typeKey)
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()