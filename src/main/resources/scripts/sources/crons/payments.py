from java.util import Date
from java.util import Calendar


class CronPayment(Container):
    def __init__(self):
        self.getToday()
        self._toFire = self.getSchedulersToFire()
        for scheduler in self._toFire:
            if not self.alreadyFired(scheduler):
                self.fireScheduler(scheduler)
                
    def getToday(self):
        calendar = Calendar.getInstance()
        calendar.setTime(Date())
        self._year = calendar.get(Calendar.YEAR)
        self._month = (calendar.get(Calendar.MONTH) + 1)
        self._day = calendar.get(Calendar.DAY_OF_MONTH)
    
    def getSchedulersToFire(self):
        sql = 'Select ps From PaymentScheduler ps Where day = %s' % self._day
        return entityManager.createQuery(sql).getResultList()
    
    def alreadyFired(self, scheduler):
        return self.findLog(scheduler) == None
    
    def fireScheduler(self, scheduler):
        for possession in scheduler.getCommunity().getPossessions()
    
    def findLog(self, scheduler):
        try:
            sql = 'Select log From PaymentSchedulerLog log Where firedYear = %s And firedMonth = %s' % (self._year, self._month)
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None