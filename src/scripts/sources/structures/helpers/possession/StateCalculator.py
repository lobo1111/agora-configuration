from base.Container import Container
from documents.helpers.Calculator import Calculator
from documents.Document import DocumentManager
from reports.ZpksStatusReport import ZpksStatusReport
from structures.BookingPeriod import BookingPeriodManager
from java.util import Date
from java.text import SimpleDateFormat
from java.math import BigDecimal
from java.math import RoundingMode

class StateCalculator(Container):
    
    def setPossession(self, possession):
        self._possession = possession
    
    def calculateCurrentRentState(self):
        status = ZpksStatusReport()
        debit, credit = status.calculate(DocumentManager().findZpk(self._possession.getZpks(), "POSSESSION"), SimpleDateFormat('dd-MM-yyyy').format(Date()))
        return credit.subtract(debit).setScale(2, RoundingMode.HALF_UP).toString()
    
    def calculateCurrentRFState(self):
        status = ZpksStatusReport()
        debit, credit = status.calculate(DocumentManager().findZpk(self._possession.getZpks(), "POSSESSION_REPAIR_FUND"), SimpleDateFormat('dd-MM-yyyy').format(Date()))
        return credit.subtract(debit).setScale(2, RoundingMode.HALF_UP).toString()
    
    def calculateRentCharging(self):
        if self.alreadyCharged():
            return 0.00
        else:
            sum = BigDecimal(0)
            calculator = Calculator()
            for element in self._possession.getElements():
                if not self.isRepairFundElement(element):
                    sum = sum.add(BigDecimal(calculator.calculate(element.getElement(), self._possession)))
            return sum.setScale(2, RoundingMode.HALF_UP).toString()
    
    def calculateRFCharging(self):
        if self.alreadyCharged():
            return 0.00
        else:
            sum = BigDecimal(0)
            calculator = Calculator()
            for element in self._possession.getElements():
                if self.isRepairFundElement(element):
                    sum = sum.add(BigDecimal(calculator.calculate(element.getElement(), self._possession)))
            return sum.setScale(2, RoundingMode.HALF_UP).toString()
    
    def isRepairFundElement(self, element):
        groupId = element.getGroup().getId()
        rfGroup = self.findBy("Dictionary", "key", "'elements.repairFundGroup'")
        return groupId == int(rfGroup.getValue())
    
    def alradyCharged(self):
        currentMonth = BookingPeriodManager().getCurrentMonth()
        lastChargedMonth = self.getLastChargedMonth()
        return currentMonth == lastChargedMonth
    
    def getLastChargedMonth(self):
        sql = "Select pos from Document doc Join doc.positions pos Where doc.possession.id = %d and doc.type = 'CHARGING' and pos.bookingPeriod.defaultPeriod = true order by pos.createdAt desc"
        return self._entityManager.createQuery(sql).getResultList().get(0).getMonth()