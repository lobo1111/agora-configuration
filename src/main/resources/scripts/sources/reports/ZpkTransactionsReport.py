from reports.Report import Report
from java.text import SimpleDateFormat
from java.util import Date
from java.util import HashMap
from java.math import BigDecimal
from java.math import RoundingMode
from javax.persistence import TemporalType

class ZpkTransactionsReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._from = self._svars.get('from')
        self._to = self._svars.get('to')
        self._zpk = self.findById("ZakladowyPlanKont", self._svars.get('zpkId'))
        self._transactions = []
        
    def collectZpks(self, zpks):
        output = []
        for zpk in zpks:
            tmp = HashMap()
            tmp.put('number', zpk.getType().getKey() + "-" + zpk.getNumber())
            debit, credit = self.calculate(zpk, self._statusDate)
            tmp.put('debit', debit)
            tmp.put('credit', credit)
            tmp.put('description', self.obtainDescription(zpk))
            output.append(tmp)
        output = sorted(output, key=lambda item: item.get('number'))
        return output
    
    def fillTemplate(self):
        self._context.put("community", self._community)
        self._context.put("fromDate", self._from)
        self._context.put("toDate", self._to)
        self._context.put("zpk", self._zpk)
        self._context.put("labelDocumentCreationDate", self._label.get('report.documentCreationDate'))
        self._context.put("labelZpkTransactions", self._label.get('report.zpkTransactions'))
        self._context.put("labelCommunity", self._label.get('report.community'))
        self._context.put("labelAddress", self._label.get('report.address'))
        self._context.put("labelZpk", self._label.get('report.zpk'))
        self._context.put("labelFromDate", self._label.get('report.from'))
        self._context.put("labelToDate", self._label.get('report.to'))
        self._context.put("labelType", self._label.get('report.documentType'))
        self._context.put("labelSubject", self._label.get('report.subject'))
        self._context.put("labelCreatedAt", self._label.get('report.createdAt'))
        self._context.put("labelValue", self._label.get('report.value'))
        self._context.put("labelDebit", self._label.get('report.debit'))
        self._context.put("labelCredit", self._label.get('report.credit'))
        self._context.put("labelDescription", self._label.get('report.description'))
        
    def getTemplateName(self):
        return "report-zpk-transactions"