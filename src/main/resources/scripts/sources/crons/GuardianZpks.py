from base.Container import Container

class GuardianZpk(Container):
    
    def checkAll(self):
        self._logger.info("Checking for wrongly calculated zpk balance...")
        for zpk in self.collect():
            self.checkZpk(zpk)
        self._logger.info("Zpk balances checked.")    
            
    def checkZpk(self, zpk):
        balance = zpk.getCurrentBalance();
        calculatedCredit = self.sumCredit(zpk.getId()) + balance.getStartCredit()
        calculatedDebit = self.sumDebit(zpk.getId()) + balance.getStartDebit()
        expectedCredit = balance.getCredit()
        expectedDebit = balance.getDebit()
        if expectedCredit != calculatedCredit:
            self._logger.info("On zpk %d found wrongly calculated credit:" % zpk.getId())
            self._logger.info("\\t calculated: %f" % calculatedCredit)
            self._logger.info("\\t expected: %f" % expectedCredit)
        if expectedDebit != calculatedDebit:
            self._logger.info("On zpk %d found wrongly calculated debit:" % zpk.getId())
            self._logger.info("\\t calculated: %f" % calculatedDebit)
            self._logger.info("\\t expected: %f" % expectedDebit)
            
    def sumCredit(self, zpkId):
        sql = "Select sum(e.value) From DocumentPosition e Where e.creditZpk.id = %d and e.booked = 1 and e.bookingPeriod.defaultPeriod = 1" % zpkId
        result = self._entityManager.createQuery(sql).getSingleResult()
        if result == None:
            return 0
        else:
            return float(int(result.floatValue() * 100)) / 100
    
    def sumDebit(self, zpkId):
        sql = "Select sum(e.value) From DocumentPosition e Where e.debitZpk.id = %d and e.booked = 1 and e.bookingPeriod.defaultPeriod = 1" % zpkId
        result = self._entityManager.createQuery(sql).getSingleResult()
        if result == None:
            return 0
        else:
            return float(int(result.floatValue() * 100)) / 100
            
    def collect(self):
        sql = "Select e From ZakladowyPlanKont e"
        return self._entityManager.createQuery(sql).getResultList()