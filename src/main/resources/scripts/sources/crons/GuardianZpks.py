class GuardianZpk(Container):
    
    def checkAll(self):
        for zpk in self.collect():
            self.checkZpk(zpk)
            
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
        sql = "Select sum(e.credit) From ZpkBalance e join e.zpk where zpk.id = %d Where e.bookingPeriod.default = 1" % zpkId
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def sumDebit(self, zpkId):
        sql = "Select sum(e.debit) From ZpkBalance e join e.zpk where zpk.id = %d Where e.bookingPeriod.default = 1" % zpkId
        return self._entityManager.createQuery(sql).getSingleResult()
            
    def collect(self):
        sql = "Select e From ZakladowyPlanKont e"
        return self._entityManager.createQuery(sql).getResultList()