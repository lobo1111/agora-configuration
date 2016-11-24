from reports.Report import Report
from java.math import BigDecimal
from javax.persistence import TemporalType
from structures.BookingPeriod import BookingPeriodManager
from java.text import SimpleDateFormat
from java.util import Date
from reports.ZpksStatusReport import ZpksStatusReport

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
        self._logger.info("Debit and Credit starting point: %s, %s" % (currentDebit.toString(), currentCredit.toString()))
        for transaction in self.getQuery().getResultList():
            item = self.getItemInstance(transaction, output)
            item['typeKey'] = transaction.getDocument().getType()
            item['type'] = self.getType(transaction)
            item['subject'] = self.getSubject(transaction)
            item['createdAt'] = SimpleDateFormat('dd-MM-yyyy').format(transaction.getCreatedAt())
            item['value'] = item['value'].add(transaction.getValue())
            item['zpkDebitId'] = transaction.getDebitZpk().getId()
            item['zpkCreditId'] = transaction.getCreditZpk().getId()
            item['zpkDebit'] = transaction.getDebitZpk().getLabel()
            item['zpkCredit'] = transaction.getCreditZpk().getLabel()
            item['month'] = transaction.getMonth()
            item['period'] = transaction.getBookingPeriod().getId()
        for item in output:
            if self._zpk.getId() == item['zpkDebitId']:
                currentDebit = item['zpkDebitStatus'] = currentDebit.add(item['value'])
                item['zpkCreditStatus'] = currentCredit
            else:
                item['zpkDebitStatus'] = currentDebit
                currentCredit = item['zpkCreditStatus'] = currentCredit.add(item['value'])
        return output

    def getItemInstance(self, transaction, output):
        for item in output:
            type = item['typeKey'] == transaction.getDocument().getType()
            date = item['createdAt'] == SimpleDateFormat('dd-MM-yyyy').format(transaction.getCreatedAt())
            debit = item['zpkDebitId'] == transaction.getDebitZpk().getId()
            credit = item['zpkCreditId'] == transaction.getCreditZpk().getId()
            month = item['month'] == transaction.getMonth()
            period = item['period'] == transaction.getBookingPeriod().getId()
            if type and date and debit and credit and month and period:
               self._logger.info("Reusing existing item to merge similar positions...")
               return item
        self._logger.info("Creating new item...")
        item = dict([])
        item['value'] = BigDecimal(0)
        output.append(item)
        return item
    
    def calculateCurrentStatus(self):
        return ZpksStatusReport().calculate(self._zpk, self._from)
    
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
            return transaction.getDocument().getPossession().getFullAddress() + " - " + transaction.getDocument().getPossession().getOwnersAsString()
        elif transaction.getDocument().getContractor() != None:
            return transaction.getDocument().getContractor().getName()
        else:
            return ""
    
    def calculateDebitStatus(self, currentDebit, transaction):
        if self._zpk.getId() == transaction.getDebitZpk().getId():
            self._logger.info("Debit change by %s, to %s" % (transaction.getValue().toString(), currentDebit.add(transaction.getValue()).toString()))
            return currentDebit.add(transaction.getValue())
        else:
            return currentDebit
    
    def calculateCreditStatus(self, currentCredit, transaction):
        if self._zpk.getId() == transaction.getCreditZpk().getId():
            self._logger.info("Credit change by %s, to %s" % (transaction.getValue().toString(), currentCredit.add(transaction.getValue()).toString()))
            return currentCredit.add(transaction.getValue())
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