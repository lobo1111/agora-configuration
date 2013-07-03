from java.util import Date
from java.util import Calendar
from java.math import BigDecimal
from java.math import RoundingMode
from pl.reaper.container.data import Payment
from pl.reaper.container.data.Payment import Direction
from pl.reaper.container.data import PaymentSchedulerLog
import re

class PaymentAlgorithm:
    def capitalize(line):
        return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])
    
    def getAttributeValue(self, instance, attribute):
        method = getattr(instance, 'get' + self.capitalize(attribute))
        result = method()
        floatValueMethod = getattr(result, 'floatValue')
        if floatValueMethod is None:
            return result
        else:
            return floatValueMethod()
    
    def calculate(self, scheduler, possession):
        entities = {"scheduler" : scheduler.getPaymentSchedulerTemplates().get(0), "possession" : possession}
        algorithm = scheduler.getPaymentSchedulerTemplates().get(0).getAlgorithm().getAlgorithm()
        occurences = re.findall('#\{(.+?)\.(.+?)\}', algorithm)
        for occurence in occurences:
            entity = occurence[0]
            attribute = occurence[1]
            instance = entities.get(entity)
            value = self.getAttributeValue(instance, attribute)
            algorithm = algorithm.replace('#{' + entity + '.' + attribute + '}', str(value))
        print algorithm
        return eval(algorithm)

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
        paymentAlgorithm = PaymentAlgorithm()
        for zpk in self.getSchedulerZpks(scheduler):
            self._logger.info('Creating payment for zpk %s' % str(zpk.getNumber()))
            payment = Payment()
            payment.setIncome(BigDecimal(paymentAlgorithm.calculate(scheduler, zpk.getPossession())).setScale(2, RoundingMode.HALF_UP))
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
        
    def getSchedulerZpks(self, scheduler):
        if scheduler.getPaymentSchedulerTemplates().get(0).getPrefix() is None:
            return scheduler.getZpks()
        else:
            sql = "Select z From ZakladowyPlanKont z Join z.community c Where z.number like '%s' and c.id = %d" % (scheduler.getPaymentSchedulerTemplates().get(0).getPrefix() + "%", scheduler.getCommunity().getId())
            return entityManager.createQuery(sql).getResultList()
        
    def addLog(self, scheduler):
        log = PaymentSchedulerLog()
        log.setPaymentScheduler(scheduler)
        log.setFiredMonth(str(self._month))
        log.setFiredYear(str(self._year))
        log.setTimestamp(Date())
        entityManager.persist(log)
    
    def findLog(self, scheduler):
        try:
            sql = 'Select log From PaymentSchedulerLog log Join log.paymentScheduler ps Where ps.id = %s And log.firedYear = %s And log.firedMonth = %s' % (scheduler.getId(), self._year, self._month)
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None
        
    def getPaymentStatus(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_STATUS', 'NEW_PAYMENT')
        