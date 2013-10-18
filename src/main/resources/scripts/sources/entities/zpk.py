from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from java.lang import Double

import sys

class ZpkManager(Container):
    _logger = Logger([:_scriptId])
    
    def setAllBookingPeriods(self, zpk):
        bookingPeriodManager = BookingPeriodManager()
        for bookingPeriod in bookingPeriodManager.findAllBookingPeriods():
            zpkBalance = self.createBalanceForPeriod(bookingPeriod)
            zpkBalance.setZpk(zpk)
            zpk.getZpkBalances().add(zpkBalance)
            
    def createBalanceForPeriod(self, bookingPeriod):
        balance = ZpkBalance()
        balance.setBookingPeriod(bookingPeriod)
        if bookingPeriod.isDefaultPeriod():
            balance.setCredit(Double.parseDouble(vars.get('credit')))
            balance.setDebit(Double.parseDouble(vars.get('debit')))
            balance.setStartCredit(Double.parseDouble(vars.get('credit')))
            balance.setStartDebit(Double.parseDouble(vars.get('debit')))
        return balance
    
    def generateZpkForPossession(self, possession):
        pool = self.findPossessionPool()
        number = self.generateNumber(pool, possession.getCommunity())
        self._logger.info("ZPK number generated: %s" % number)
        zpk = ZakladowyPlanKont()
        zpk.setNumber(number)
        zpk.setCommunity(possession.getCommunity())
        zpk.setPossession(possession)
        zpk.setType(pool)
        vars.put('credit', '0')
        vars.put('debit', '0')
        self.setAllBookingPeriods(zpk)
        return zpk
    
    def save(self, zpk):
        self._logger.info(zpk.longDescription())
        entityManager.persist(zpk)
    
    def findPossessionPool(self):
        return entityManager.createQuery("SELECT dict FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = 'ZPKS_SETTINGS' AND dict.key = 'POSSESSION'").getSingleResult()
    
    def generateNumber(self, dict, community):
        zpks = []
        for zpk in community.getZpks():
            if(zpk.getType().getId() == dict.getId()):
                zpks.append(int(zpk.getNumber()))
        for i in range(1, 1000):
            if not i in zpks:
                return self.parseNumber(i)
        return '0'
            
    def parseNumber(self, i):
        if i < 10:
            return '00' + str(i)
        elif i < 100:
            return '0' + str(i)
        return str(i)
            