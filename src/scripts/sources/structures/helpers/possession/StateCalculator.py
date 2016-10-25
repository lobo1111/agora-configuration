from documents.Document import DocumentManager
from reports.ZpksStatusReport import ZpksStatusReport
from java.util import Date

class StateCalculator():
    
    def __init__(self, possession):
        self._possession = possession
    
    def calculateCurrentRentState(self):
        status = ZpksStatusReport()
        debit, credit = status.calculate(DocumentManager().findZpk(self._possession.getZpks(), "POSSESSION"), Date())
        return credit - debit
    
    def calculateCurrentRFState(self):
        status = ZpksStatusReport()
        debit, credit = status.calculate(DocumentManager().findZpk(self._possession.getZpks(), "POSSESSION_REPAIR_FUND"), Date())
        return credit - debit
    
    def calculateRentCharging(self):
        return 1
    
    def calculateRFCharging(self):
        return 1
    