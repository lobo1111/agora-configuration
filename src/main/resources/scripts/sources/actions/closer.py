class Close:
    _logger = Logger([:_scriptId])
    
    def canCloseMonth(self):
        self._currentMonth = self.getCurrentMonth()
        if self._currentMonth < '12':
            return True
        else:
            return False
        
    def closeMonth(self):
        if self.canCloseMonth():
            self._logger.info('Closing month...')
            self.clearQueue()
            self.setNextMonth()
            self._logger.info('Month closed')
        else:
            self._logger.info("Month can't be closed - its already 12")
        
    def getCurrentMonth(self):
        return entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
        
    def clearQueue(self):
        entityManager.createQuery("Delete From ChargingQueue cq").executeQuery()
        self._logger.info('Charge queue cleared')
        
    def setNextMonth(self):
        self._currentMonth += 1
        self._logger.info('Setting current month as %s' % str(self._currentMonth))
        entityManager.createQuery('Update Dictionary Set dict.value = "%s" Where dict.id IN (SELECT dict.id FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT")' % str(self._currentMonth)).executeQuery()
        self._logger.info('Next month set')