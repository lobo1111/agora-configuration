from documents.Document import Document
from reports.ZpksStatusReport import ZpksStatusReport

class StateCalculator():
    
    def __init__(self, possession):
        self._possession = possession
    
    def calculateCurrentRentState(self):
        status = ZpksStatusReport()
        debit, credit = status.calculate(Document().findZpk(self._possession.getZpks(), "POSSESSION"), Date())
        return credit - debit
    
    def calculateCurrentRFState(self):
        status = ZpksStatusReport()
        debit, credit = status.calculate(Document().findZpk(self._possession.getZpks(), "POSSESSION_REPAIR_FUND"), Date())
        return credit - debit
    
    def calculateRentCharging(self):
        return 1
    
    def calculateRFCharging(self):
        return 1
    