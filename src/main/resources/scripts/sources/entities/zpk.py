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
            entityManager.persist(zpkBalance)
            
    def createBalanceForPeriod(self, bookingPeriod):
        balance = ZpkBalance()
        balance.setBookingPeriod(bookingPeriod)
        if  bookingPeriod.isDefaultPeriod():
            balance.setCredit(Double.parseDouble(vars.get(self._prefix + 'credit')))
            balance.setDebit(Double.parseDouble(vars.get(self._prefix + 'debit')))
            balance.setStartCredit(Double.parseDouble(vars.get(self._prefix + 'credit')))
            balance.setStartDebit(Double.parseDouble(vars.get(self._prefix + 'debit')))
        return balance
    
    def generateZpkForPossession(self, possession):
        pool = self.findPossessionPool()
        number = self.generateNumber(pool, possession.getCommunity())
        zpk = ZakladowyPlanKont()
        zpk.setNumber(number)
        zpk.setCommunity(possession.getCommunity())
        zpk.setPossession(possession)
        zpk.setType(pool)
        entityManager.persist(zpk)
        return zpk
    
    def findPossessionPool(self):
        return entityManager.createQuery("SELECT dict FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = 'ZPKS_SETTINGS' AND dict.key = 'POSSESSION'").getSingleResult()
    
    def generateNumber(self, dict, community):
        zpks = []
        for zpk in community.getZpks():
            zpks.append(int(zpk.getNumber()))
        for i in range(0, 1000):
            if not i in zpks:
                return self.parseNumber(i)
        return 0
            
    def parseNumber(self, i):
        if i < 10:
            return '00' + str(i)
        elif i < 100:
            return '0' + str(i)
        return i
            