from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from java.lang import Double

class ZpkManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        zpk = ZakladowyPlanKont()
        self.setZpkData(zpk)
        self.saveZpk(zpk)
        return zpk
        
    def setZpkData(self, zpk):
        zpk.setNumber(vars.get('number'))
        zpk.setDescription(vars.get('description'))
        zpk.setCommunity(self.getCommunity(zpk))
        zpk.setPossession(self.getPossession(zpk))
        zpk.setObligation(self.getObligation(zpk))
        self.setAllBookingPeriods(zpk)
        
    def getCommunity(self, zpk):
        if 'communityId' in vars and vars.get('communityId') != '0':
            communityManager = CommunityManager()
            return communityManager.findCommunityById(vars.get('communityId'))
        
    def getPossession(self, zpk):
        if 'possessionId'in vars and vars.get('possessionId') != '0':
            possessionManager = PossessionManager()
            return possessionManager.findPossessionById(vars.get('possessionId'))
        
    def getObligation(self, zpk):
        if 'obligationId' in vars and vars.get('obligationId') != '0':
            return entityManager.createQuery('Select o From Obligation o Where o.id = ' + str(vars.get('obligationId'))).getSingleResult()
        
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
            balance.setCredit(Double.parseDouble(vars.get('credit')))
            balance.setDebit(Double.parseDouble(vars.get('debit')))
            balance.setStartCredit(Double.parseDouble(vars.get('credit')))
            balance.setStartDebit(Double.parseDouble(vars.get('debit')))
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
        