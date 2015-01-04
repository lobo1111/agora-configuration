from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from java.lang import Double
from base.Container import Container
from entities.BookingPeriod import BookingPeriodManager

class ZpkManager(Container):

    def create(self):
        pool = self.findPool(self._svars.get('poolId'))
        community = self.findCommunityById(self._svars.get('communityId'))
        number = self.generateNumber(pool, community)
        zpk = ZakladowyPlanKont()
        zpk.setNumber(number)
        zpk.setCommunity(community)
        community.getZpks().add(zpk)
        zpk.setType(pool)
        self._svars.put('credit', '0')
        self._svars.put('debit', '0')
        self.setAllBookingPeriods(zpk)
        return zpk
    
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
            balance.setCredit(Double.parseDouble(self._svars.get('credit')))
            balance.setDebit(Double.parseDouble(self._svars.get('debit')))
            balance.setStartCredit(Double.parseDouble(self._svars.get('credit')))
            balance.setStartDebit(Double.parseDouble(self._svars.get('debit')))
        return balance
    
    def generateZpkForCommunity(self, community, poolKey, credit = '0', debit = '0'):
        poolId = self.findPoolId(poolKey)
        pool = self.findPool(poolId.getValue())
        number = self.generateNumber(pool, community)
        self._logger.info("ZPK number generated: %s" % number)
        zpk = ZakladowyPlanKont()
        zpk.setNumber(number)
        zpk.setCommunity(community)
        community.getZpks().add(zpk)
        zpk.setType(pool)
        self._svars.put('credit', credit)
        self._svars.put('debit', debit)
        self.setAllBookingPeriods(zpk)
        return zpk

    def save(self, zpk):
        self._logger.info(zpk.longDescription())
        self._entityManager.persist(zpk)

    def findPoolByName(self, poolName):
        poolId = self.findPoolId(poolName)
        return self.findPool(poolId)

    def findPool(self, poolId):
        sql = "SELECT d FROM Dictionary d WHERE d.id = %s" % str(poolId)
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def findPoolId(self, poolName):
        return self._entityManager.createQuery("SELECT dict FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = 'ZPKS_SETTINGS' AND dict.key = '%s'" % poolName).getSingleResult()
    
    def findCommunityById(self, communityId):
        sql = "SELECT c FROM Community c WHERE c.id = %s" % str(communityId)
        return self._entityManager.createQuery(sql).getSingleResult()

    def generateNumber(self, dict, community):
        zpks = []
        for zpk in community.getZpks():
            if(zpk.getType().getId() == dict.getId()):
                zpks.append(int(zpk.getNumber()))
                self._logger.info('Number already taken from the pool %d' % int(zpk.getNumber()))
        for i in range(1, 1000):
            if not i in zpks:
                self._logger.info('Number %d looks free' % i)
                return self.parseNumber(i)
        return '0'
            
    def parseNumber(self, i):
        if i < 10:
            return '00' + str(i)
        elif i < 100:
            return '0' + str(i)
        return str(i)

    def setStartBalance(self):
        zpk = self.findById('ZakladowyPlanKont', self._svars.get('id'))
        balance = zpk.getCurrentBalance()
        credit = float(self._svars.get('credit'))
        debit = float(self._svars.get('debit'))
        self.revokeOldStartBalance(balance)
        self.setNewStartBalance(balance, credit, debit)
        self.saveEntity(balance)

    def revokeOldStartBalance(self, balance):
        credit = balance.getStartCredit()
        debit = balance.getStartDebit()
        balance.setStartCredit(0)
        balance.setStartDebit(0)
        balance.setCredit(balance.getCredit() - credit)
        balance.setDebit(balance.getDebit() - debit)
            
    def setNewStartBalance(self, balance, credit, debit):
        balance.setStartCredit(credit)
        balance.setStartDebit(debit)
        balance.setCredit(balance.getCredit() + credit)
        balance.setDebit(balance.getDebit() + debit)
