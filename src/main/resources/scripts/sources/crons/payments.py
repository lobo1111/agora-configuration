from java.util import Date
from java.util import Calendar
from java.math import BigDecimal
from pl.reaper.container.data import Payment
from pl.reaper.container.data import PaymentSchedulerLog

class CronPayment(Container):
    def __init__(self):
        self._dictManager = DictionaryManager()
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
        sql = 'Select ps From PaymentScheduler ps Where ps.day = %s' % self._day
        return entityManager.createQuery(sql).getResultList()
    
    def alreadyFired(self, scheduler):
        return self.findLog(scheduler) == None
    
    def fireScheduler(self, scheduler):
        for zpk in scheduler.getZpks():
            payment = Payment()
            self.setAmount(payment, scheduler.getPaymentSchedulerTemplates().get(0).getAmount())
            payment.setType(scheduler.getPaymentSchedulerTemplates().get(0).getType())
            payment.setStatus(self.getPaymentStatus())
            payment.setDescription(scheduler.getPaymentSchedulerTemplates().get(0).getDescription())
            payment.setCreateDay(Date())
            payment.setDirection("EXPENDITURE")
            if scheduler.getPaymentSchedulerTemplates().get(0).isAutoBook():
                vars.set('zpkId', str(zpk.getId()))
                vars.set('paymentBookingPeriod', BookingPeriodManager().findDefaultBookingPeriod())
                BookingManager().book(payment)
            entityManager.persist(payment)
        self.addLog(scheduler)
        
    def addLog(self, scheduler):
        log = PaymentSchedulerLog()
        log.setPaymentScheduler(scheduler)
        log.setFiredMonth(self._month)
        log.setFiredYear(self._year)
        log.setTimestamp(Date())
        entityManager.persist(log)
            
    def setIncome(self, payment, factor):
        calculated = factor * zpk.getPossession().getArea()
        payment.setIncome(BigDecimal(calculated))
    
    def findLog(self, scheduler):
        try:
            sql = 'Select log From PaymentSchedulerLog log Where log.firedYear = %s And log.firedMonth = %s' % (self._year, self._month)
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None
        
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'NEW_PAYMENT')
        