from java.util import Date
from java.util import Calendar
from java.math import BigDecimal
from pl.reaper.container.data import Payment
from pl.reaper.container.data.Payment import Direction
from pl.reaper.container.data import PaymentSchedulerLog

class CronPayment(Container):
    _logger = Logger([:_scriptId])
    
    def __init__(self):
        self._logger.info('Cron payment started...')
        self._dictManager = DictionaryManager()
        self.getToday()
        self._toFire = self.getSchedulersToFire()
        self._logger.info('Found %s active and ready to fire schedulers' % (str(self._toFire.size())))
        for scheduler in self._toFire:
            self._logger.info('Checking scheduler %s' % scheduler.getName())
            if not self.alreadyFired(scheduler):
                self._logger.info('Scheduler not fired yet...')
                self.fireScheduler(scheduler)
            else:
                self._logger.info('Scheduler already fired, omitting.')
        self._logger.info('Cron payment finished.')
            
                
    def getToday(self):
        calendar = Calendar.getInstance()
        calendar.setTime(Date())
        self._year = calendar.get(Calendar.YEAR)
        self._month = (calendar.get(Calendar.MONTH) + 1)
        self._day = calendar.get(Calendar.DAY_OF_MONTH)
    
    def getSchedulersToFire(self):
        sql = 'Select ps From PaymentScheduler ps Where ps.day = %s and ps.active = true' % self._day
        return entityManager.createQuery(sql).getResultList()
    
    def alreadyFired(self, scheduler):
        return self.findLog(scheduler) != None
    
    def fireScheduler(self, scheduler):
        for zpk in scheduler.getZpks():
            self._logger.info('Creating payment for zpk %s' % str(zpk.getNumber()))
            payment = Payment()
            self.setAmount(zpk, payment, scheduler.getPaymentSchedulerTemplates().get(0).getAmount())
            payment.setCommunity(scheduler.getCommunity())
            payment.setPossession(zpk.getPossession())
            payment.setType(scheduler.getPaymentSchedulerTemplates().get(0).getType())
            payment.setStatus(self.getPaymentStatus())
            payment.setDescription(scheduler.getPaymentSchedulerTemplates().get(0).getDescription())
            payment.setCreateDay(Date())
            payment.setDirection(Direction.EXPENDITURE)
            if scheduler.getPaymentSchedulerTemplates().get(0).isAutoBook():
                vars.put('zpkId', str(zpk.getId()))
                vars.put('paymentBookingPeriod', BookingPeriodManager().findDefaultBookingPeriod().getId())
                BookingManager().book(payment)
            entityManager.persist(payment)
        self.addLog(scheduler)
        
    def addLog(self, scheduler):
        log = PaymentSchedulerLog()
        log.setPaymentScheduler(scheduler)
        log.setFiredMonth(str(self._month))
        log.setFiredYear(str(self._year))
        log.setTimestamp(Date())
        entityManager.persist(log)
            
    def setAmount(self, zpk, payment, factor):
        calculated = factor.floatValue() * zpk.getPossession().getArea().floatValue()
        self._logger.info('calculated payment - %s' % str(calculated))
        payment.setIncome(BigDecimal(calculated))
    
    def findLog(self, scheduler):
        try:
            sql = 'Select log From PaymentSchedulerLog log Join log.paymentScheduler ps Where ps.id = %s And log.firedYear = %s And log.firedMonth = %s' % (scheduler.getId(), self._year, self._month)
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None
        
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'NEW_PAYMENT')
        