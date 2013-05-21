from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from java.lang import Double

class ZpkManager(Container):
    _logger = Logger([:_scriptId])
    
    def setPrefix(self, prefix):
        self._prefix = prefix
    
    def create(self):
        zpk = ZakladowyPlanKont()
        self.setZpkData(zpk)
        self.saveZpk(zpk)
        return zpk
        
    def setZpkData(self, zpk):
        zpk.setNumber(vars.get(self._prefix + 'number'))
        zpk.setDescription(vars.get(self._prefix + 'description'))
        zpk.setCommunity(self.getCommunity(zpk))
        zpk.setPossession(self.getPossession(zpk))
        zpk.setObligation(self.getObligation(zpk))
        self.setAllBookingPeriods(zpk)
        
    def getCommunity(self, zpk):
        return CommunityManager().findCommunityById(vars.get(self._prefix + 'communityId'))
        
    def getPossession(self, zpk):
        if (self._prefix + 'possessionId') in vars and vars.get(self._prefix + 'possessionId') != '0':
            possessionManager = PossessionManager()
            return possessionManager.findPossessionById(vars.get(self._prefix + 'possessionId'))
        
    def getObligation(self, zpk):
        if (self._prefix + 'obligationId') in vars and vars.get(self._prefix + 'obligationId') != '0':
            return entityManager.createQuery('Select o From Obligation o Where o.id = ' + str(vars.get(self._prefix + 'obligationId'))).getSingleResult()
        
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
        
    def saveZpk(self, zpk):
        self._logger.info(zpk.longDescription())
        entityManager.persist(zpk)
        entityManager.flush()
        
    def findZpkById(self, id):
        sql = "Select zpk From ZakladowyPlanKont zpk Where zpk.id = '%s'" % id
        return entityManager.createQuery(sql).getSingleResult()
    
    def findBalanceByZpkAndPeriod(self, zpk, period):
        sql = "Select balance From ZpkBalance balance Where balance.zpk.id = '%s' and balance.bookingPeriod.id = '%s'" % (zpk.getId(), period.getId())
        return entityManager.createQuery(sql).getSingleResult()
        