from reports.Report import Report
from javax.persistence import TemporalType
from structures.BookingPeriod import BookingPeriodManager
from java.text import SimpleDateFormat
from java.util import Date

class ZpkTransactionsReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._from = self.getFrom()
        self._to = self.getTo()
        self._zpk = self.findById("ZakladowyPlanKont", self._svars.get('zpkId'))
        self._transactions = self.collectTransactions()
        
    def collectTransactions(self):
        output = []
        currentDebit, currentCredit = self.calculateCurrentStatus()
        for transaction in self.getQuery().getResultList():
            item = dict([])
            item['type'] = self.getType(transaction)
            item['subject'] = self.getSubject(transaction)
            item['createdAt'] = SimpleDateFormat('dd-MM-yyyy').parse(transaction.getCreatedAt())
            item['value'] = transaction.getValue()
            item['zpkDebit'] = transaction.getDebitZpk().getLabel()
            item['zpkCredit'] = transaction.getCreditZpk().getLabel()
            currentDebit = self.calculateDebitStatus(currentDebit, transaction)
            currentCredit = self.calculateCreditStatus(currentCredit, transaction)
            item['zpkDebitStatus'] = currentDebit
            item['zpkCreditStatus'] = currentCredit
        output.append(item)
        return output
    
    def calculateCurrentStatus(self):
        return 0, 0
    
    def getType(self, transaction):
        if transaction.getDocument().getType() == "INVOICE":
            return self._label.get('document.invoice')
        elif transaction.getDocument().getType() == "BANK_NOTE":
            return self._label.get('document.bankNote')
        elif transaction.getDocument().getType() == "ACCOUNT_PROVISION":
            return self._label.get('document.accountProvision')
        elif transaction.getDocument().getType() == "POSSESSION_PAYMENT":
            return self._label.get('document.possessionPayment')
        elif transaction.getDocument().getType() == "CHARGING":
            return self._label.get('document.charging')
    
    def getSubject(self, transaction):
        if transaction.getDocument().getPossession() != None:
            return transaction.getDocument().getPossession().getFullAddress()
        elif transaction.getDocument().getContractor() != None:
            return transaction.getDocument().getContractor().getName()
        else:
            return ""
    
    def calculateDebitStatus(self, currentDebit, transaction):
        if self._zpk.getId() == transaction.getDebitZpk().getId():
            return currentDebit + transaction.getValue()
        else:
            return currentDebit
    
    def calculateCreditStatus(self, currentCredit, transaction):
        if self._zpk.getId() == transaction.getCreditZpk().getId():
            return currentCredit + transaction.getValue()
        else:
            return currentCredit
    
    def getQuery(self):
        sql = "Select dp From DocumentPosition dp Where (dp.debitZpk.id = :did or dp.creditZpk.id = :cid) and dp.bookingPeriod.defaultPeriod = 1 and dp.createdAt >= :from and dp.createdAt <= :to Order By dp.createdAt ASC"
        query = self._entityManager.createQuery(sql)
        query.setParameter("did", self._zpk.getId())
        query.setParameter("cid", self._zpk.getId())
        query.setParameter("from", SimpleDateFormat('dd-MM-yyyy').parse(self._from), TemporalType.DATE)
        query.setParameter("to", SimpleDateFormat('dd-MM-yyyy').parse(self._to), TemporalType.DATE)
        return query
    
    def getFrom(self):
        if self._svars.get('from') == '':
            year = BookingPeriodManager().findDefaultBookingPeriod().getName()
            return "01-01-%s" % year
        else:
            return self._svars.get('from')
    
    def getTo(self):
        if self._svars.get('to') == '':
            return str(SimpleDateFormat('dd-MM-yyyy').format(Date()))
        else:
            return self._svars.get('to')
    
    def fillTemplate(self):
        self._context.put("community", self._community)
        self._context.put("fromDate", self._from)
        self._context.put("toDate", self._to)
        self._context.put("zpk", self._zpk)
        self._context.put("transactions", self._transactions)
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