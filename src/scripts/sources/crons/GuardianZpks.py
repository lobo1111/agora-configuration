from base.Container import Container
from java.math import BigDecimal

class GuardianZpk(Container):
    
    def checkAll(self):
        self._logger.info("Checking for wrongly calculated zpk balance...")
        for zpk in self.collect():
            self.checkZpk(zpk)
        self._logger.info("Zpk balances checked.")    
            
    def checkZpk(self, zpk):
        balance = zpk.getCurrentBalance();
        calculatedCredit = (self.sumCredit(zpk.getId()).add(balance.getStartCredit()))
        calculatedDebit = (self.sumDebit(zpk.getId()).add(balance.getStartDebit()))
        expectedCredit = balance.getCredit()
        expectedDebit = balance.getDebit()
        if not expectedCredit.equals(calculatedCredit):
            self._logger.info("On zpk %d found wrongly calculated credit:" % zpk.getId())
            self._logger.info("calculated: %s" % calculatedCredit.toPlainString())
            self._logger.info("expected: %s" % expectedCredit.toPlainString())
        if not expectedDebit.equals(calculatedDebit):
            self._logger.info("On zpk %d found wrongly calculated debit:" % zpk.getId())
            self._logger.info("calculated: %s" % calculatedDebit.toPlainString())
            self._logger.info("expected: %s" % expectedDebit.toPlainString())
            
    def sumCredit(self, zpkId):
        sql = "Select sum(e.value) From DocumentPosition e Where e.creditZpk.id = %d and e.booked = 1 and e.bookingPeriod.defaultPeriod = 1" % zpkId
        result = self._entityManager.createQuery(sql).getSingleResult()
        if result == None:
            return BigDecimal(0)
        else:
            return result
    
    def sumDebit(self, zpkId):
        sql = "Select sum(e.value) From DocumentPosition e Where e.debitZpk.id = %d and e.booked = 1 and e.bookingPeriod.defaultPeriod = 1" % zpkId
        result = self._entityManager.createQuery(sql).getSingleResult()
        if result == None:
            return BigDecimal(0)
        else:
            return result
            
    def collect(self):
        sql = "Select e From ZakladowyPlanKont e"
        return self._entityManager.createQuery(sql).getResultList()