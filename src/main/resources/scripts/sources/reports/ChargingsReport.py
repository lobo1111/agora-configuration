from reports.Report import Report
from java.text import SimpleDateFormat
from java.util import Date
from java.util import HashMap
from java.math import BigDecimal
from java.math import RoundingMode
from javax.persistence import TemporalType

class ChargingsReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._possession = self.findById("Possession", self._svars.get('possessionId'))
        self._startBalance = self.getStartBalance()
        self._transactions = self.collectTransactions()
        
    def getStartBalance(self):
        return BigDecimal(0)
        
    def collectTransactions(self):
        output = []
        return output
    
    def fillTemplate(self):
        self._context.put("community", self._community)
        self._context.put("possession", self._possession)
        self._context.put("startBalance", self._startBalance)
        self._context.put("transactions", self._transactions)
        self._context.put("labelDocumentCreationDate", self._label.get('report.documentCreationDate'))
        self._context.put("labelChargings", self._label.get('report.chargings'))
        self._context.put("labelCommunity", self._label.get('report.community'))
        self._context.put("labelPossession", self._label.get('report.possession'))
        self._context.put("labelOwners", self._label.get('report.owners'))
        self._context.put("labelStatusDate", self._label.get('report.statusDate'))
        self._context.put("labelBalance", self._label.get('report.balance'))
        self._context.put("labelStartBalance", self._label.get('report.startBalance'))
        self._context.put("labelCreatedAt", self._label.get('report.createdAt'))
        self._context.put("labelValue", self._label.get('report.value'))
        
    def getTemplateName(self):
        return "report-zpks-status"