class Close:
    def canCloseMonth(self):
        self._currentMonth = self.getCurrentMonth()
        if self._currentMonth < 12:
            return True
        else:
            return False
        
    def closeMonth(self):
        if self.canCloseMonth():
            self.clearQueue()
            self.setNextMonth()
        
    def getCurrentMonth(self):
        return entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
        
    def clearQueue(self):
        entityManager.createQuery("Delete From ChargingQueue cq").executeQuery()
        
    def setNextMonth(self):
        self._currentMonth += 1
        entityManager.createQuery('Update Dictionary Set dict.value = "%s" Where dict.id IN (SELECT dict.id FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT")' % str(self._currentMonth)).executeQuery()