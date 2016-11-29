from reports.Report import Report
from java.text import SimpleDateFormat
from java.util import Date
from java.util import HashMap
from java.math import BigDecimal
from java.math import RoundingMode
from javax.persistence import TemporalType
from reports.Report import Report
from structures.Account import AccountManager
from structures.BookingPeriod import BookingPeriodManager
from documents.helpers.Calculator import Calculator

class BankAccountsReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._statusDate = self.getStatusDate()
        self._accounts = self.collectAccounts(self._community.getAccounts())
        
    def collectAccounts(self, accounts):
        output = []
        for account in accounts:
            item = dict([])
            item['account'] = AccountManager().makeReadable(account.getNumber())
            item['type'] = account.getType().getValue()
            totalCredit = BigDecimal(0)
            totalDebit = BigDecimal(0)
            for zpk in account.getZpks():
                debit, credit = self.calculate(zpk, self._statusDate)
                totalCredit = totalCredit.add(credit)
                totalDebit = totalDebit.add(debit)
            item['status'] = totalDebit.subtract(totalCredit).setScale(2, RoundingMode.HALF_UP)
            output.append(item)
        output = sorted(output, key=lambda item: item.get('account'))
        return output
    
    def calculate(self, zpk, statusDate):
        balance = zpk.getCurrentBalance();
        calculatedDebit = (self.sumDebit(zpk.getId(), statusDate).add(balance.getStartDebit()))
        calculatedCredit = (self.sumCredit(zpk.getId(), statusDate).add(balance.getStartCredit()))
        return calculatedDebit, calculatedCredit
    
    def sumCredit(self, zpkId, statusDate):
        date = SimpleDateFormat('dd-MM-yyyy').parse(statusDate)
        sql = "Select sum(e.value) From DocumentPosition e Where e.creditZpk.id = :debitId and e.canceled = 0 and e.bookingPeriod.defaultPeriod = 1 and e.createdAt <= :date"
        query = self._entityManager.createQuery(sql)
        query.setParameter("debitId", zpkId)
        query.setParameter("date", date, TemporalType.DATE)
        result = query.getSingleResult()
        if result == None:
            return BigDecimal(0)
        else:
            return result
    
    def sumDebit(self, zpkId, statusDate):
        date = SimpleDateFormat('dd-MM-yyyy').parse(statusDate)
        sql = "Select sum(e.value) From DocumentPosition e Where e.debitZpk.id = :debitId and e.canceled = 0 and e.bookingPeriod.defaultPeriod = 1 and e.createdAt <= :date"
        query = self._entityManager.createQuery(sql)
        query.setParameter("debitId", zpkId)
        query.setParameter("date", date, TemporalType.DATE)
        result = query.getSingleResult()
        if result == None:
            return BigDecimal(0)
        else:
            return result
        
    def getStatusDate(self):
        if self._svars.get('statusDate') == '':
            return str(SimpleDateFormat('dd-MM-yyyy').format(Date()))
        else:
            return self._svars.get('statusDate')
        
    def fillTemplate(self):
        self._context.put("community", self._community)
        self._context.put("statusDate", self._statusDate)
        self._context.put("accounts", self._accounts)
        self._context.put("labelDocumentCreationDate", self._label.get('report.documentCreationDate'))
        self._context.put("labelStatusDate", self._label.get('report.statusDate'))
        self._context.put("labelCommunity", self._label.get('report.community'))
        self._context.put("labelNumber", self._label.get('report.number'))
        self._context.put("labelDescription", self._label.get('report.description'))
        self._context.put("labelValue", self._label.get('field.value'))
        self._context.put("labelBankAccountsStatus", self._label.get('report.bankAccountsStatus'))
        
        
    def getTemplateName(self):
        return "report-bank-accounts-status"