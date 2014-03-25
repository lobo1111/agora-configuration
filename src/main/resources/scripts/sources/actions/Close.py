from base.Container import Container
from entities.Dictionary import DictionaryManager
from actions.ChargingBooker import ChargingBooker
from actions.PaymentBooker import PaymentBooker

class Close(Container):
    
    def closeMonth(self):
        self._currentMonth = int(self.getCurrentMonth())
        if self._currentMonth < 12:
            self._logger.info('Closing month...')
            self.clearQueue()
            self.bookAll()
            self.setNextMonth()
            self._logger.info('Month closed')
        else:
            self._logger.info("Month can't be closed - its already %d" % self._currentMonth)
        
    def getCurrentMonth(self):
        return entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
        
    def clearQueue(self):
        entityManager.createQuery("Delete From ChargingQueue cq").executeUpdate()
        self._logger.info('Charge queue cleared')
        
    def setNextMonth(self):
        self._currentMonth += 1
        dict = DictionaryManager().findDictionaryInstance("PERIODS", "CURRENT")
        dict.setValue(str(self._currentMonth))
        entityManager.persist(dict)
        entityManager.flush()
        
    def bookAll(self):
        ChargingBooker().bookAllChargings()
        PaymentBooker().bookAllPayments()