from pl.reaper.container.data import BookingPeriod
from pl.reaper.container.data import ZpkBalance
from base.Container import Container
from structures.Dictionary import DictionaryManager
from java.util import Calendar
import locale
import datetime

class BookingPeriodManager(Container):
    
    def findAllBookingPeriods(self):
        query = 'Select period From BookingPeriod period'
        return self._entityManager.createQuery(query).getResultList()
    
    def findDefaultBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()

    def findChild(self, bookingPeriod):
        try:
            sql = 'Select period From BookingPeriod period Where period.order = ' + str(bookingPeriod.getOrder() + 1)
            return self._entityManager.createQuery(sql).getSingleResult()
        except:
            return None

    def getCurrentMonth(self):
        return DictionaryManager().findDictionaryInstance('PERIODS', 'CURRENT')
    
    def getCurrentMonthName(self):
        monthNumber = self.getCurrentMonth().getValue()
        locale.setlocale(locale.LC_ALL, "pl_PL.ISO8859-2")
        monthName = datetime.datetime.strptime(monthNumber, "%m").strftime("%B")
        locale.setlocale(locale.getdefaultlocale())
        return monthName

    def closeYear(self):
        if self.getCurrentMonth() == '12':
            currentBookingPeriod = self.findDefaultBookingPeriod()
            newBookingPeriod = self.createBookingPeriod(currentBookingPeriod)
            [self.createBalance(zpk, newBookingPeriod) for zpk in self.collectZpks()]
            newBookingPeriod.setActive(True)
            newBookingPeriod.setDefaultPeriod(True)
            currentBookingPeriod.setActive(False)
            currentBookingPeriod.setDefaultPeriod(False)
            currentMonthInstance = self.getCurrentMonth()
            currentMonthInstance.setValue('1')
            self.saveEntity(currentMonthInstance)
            self.saveEntity(currentBookingPeriod)
            self.saveEntity(newBookingPeriod)

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

    def collectZpks(self):
        return self._entityManager.createQuery('Select z From ZakladowyPlanKont z').getResultList()
    
        
    