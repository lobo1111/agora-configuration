from pl.reaper.container.data import BookingPeriod
from pl.reaper.container.data import ZpkBalance
from base.Container import Container
from entities.Dictionary import DictionaryManager
from java.util import Calendar

class BookingPeriodManager(Container):
    
    def findAllBookingPeriods(self):
        query = 'Select period From BookingPeriod period'
        return self._entityManager.createQuery(query).getResultList()
    
    def findBookingPeriodById(self, id):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.id = ' + str(id)).getSingleResult()

    def findDefaultBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()

    def findChild(self, bookingPeriod):
        try:
            sql = 'Select period From BookingPeriod period Where period.order = ' + str(bookingPeriod.getOrder() + 1)
            return self._entityManager.createQuery(sql).getSingleResult()
        except:
            return None

    def getCurrentMonth(self):
        return self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()

    def closeYear(self):
        if self.canCloseYear():
            currentBookingPeriod = self.findDefaultBookingPeriod()
            newBookingPeriod = self.createBookingPeriod(currentBookingPeriod)
            [self.createBalance(zpk, newBookingPeriod) for zpk in self.collectZpks()]
            newBookingPeriod.setActive(True)
            newBookingPeriod.setDefaultPeriod(True)
            currentBookingPeriod.setActive(False)
            currentBookingPeriod.setDefaultPeriod(False)
            currentMonthInstance = DictionaryManager().findDictionaryInstance('PERIODS', 'CURRENT')
            currentMonthInstance.setValue('1')
            self.saveEntity(currentMonthInstance)
            self.saveEntity(currentBookingPeriod)
            self.saveEntity(newBookingPeriod)

    def canCloseYear(self):
        currentMonth = int(self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult())
        return currentMonth == 12

    def createBookingPeriod(self, currentBookingPeriod):
        bp = BookingPeriod()
        bp.setDefaultPeriod(True)
        bp.setName(str(Calendar.getInstance().get(Calendar.YEAR)))
        bp.setOrder(currentBookingPeriod.getOrder() + 1)
        self.saveEntity(bp)
        return bp

    def createBalance(self, zpk, bookingPeriod):
        currentBalance = zpk.getCurrentBalance()
        newBalance = ZpkBalance()
        newBalance.setBookingPeriod(bookingPeriod)
        newBalance.setZpk(zpk)
        zpk.getZpkBalances().add(newBalance)
        if currentBalance.getCredit() > currentBalance.getDebit():
            newBalance.setStartCredit(currentBalance.getCredit() - currentBalance.getDebit())
            newBalance.setCredit(currentBalance.getCredit() - currentBalance.getDebit())
            newBalance.setStartDebit(0)
            newBalance.setDebit(0)
        else:
            newBalance.setStartCredit(0)
            newBalance.setCredit(0)
            newBalance.setStartDebit(currentBalance.getDebit() - currentBalance.getCredit())
            newBalance.setDebit(currentBalance.getDebit() - currentBalance.getCredit())
        self.saveEntity(zpk)
        self.saveEntity(newBalance)

    def collectZpks(self):
        return self._entityManager.createQuery('Select z From ZakladowyPlanKont z').getResultList()
    
        
    