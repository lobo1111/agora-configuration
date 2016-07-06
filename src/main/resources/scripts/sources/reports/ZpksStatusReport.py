from reports.Report import Report
from java.text import SimpleDateFormat
from java.util import Date
from java.util import HashMap
from java.math import BigDecimal
from java.math import RoundingMode
from javax.persistence import TemporalType

class ZpksStatusReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._statusDate = self.getStatusDate()
        self._zpks = self.collectZpks(self._community.getZpks())
        
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
    
    def calculate(self, zpk, statusDate):
        balance = zpk.getCurrentBalance();
        calculatedDebit = (self.sumDebit(zpk.getId(), statusDate).add(BigDecimal(balance.getStartDebit()))).setScale(2, RoundingMode.HALF_UP)
        calculatedCredit = (self.sumCredit(zpk.getId(), statusDate).add(BigDecimal(balance.getStartCredit()))).setScale(2, RoundingMode.HALF_UP)
        return calculatedDebit, calculatedCredit
    
    def sumCredit(self, zpkId, statusDate):
        date = SimpleDateFormat('dd-MM-yyyy').parse(statusDate)
        sql = "Select sum(e.value) From DocumentPosition e Where e.creditZpk.id = :debitId and e.booked = 1 and e.bookingPeriod.defaultPeriod = 1 and e.createdAt <= :date"
        query = self._entityManager.createQuery(sql)
        query.setParameter("debitId", zpkId)
        query.setParameter("date", date, TemporalType.DATE)
        result = query.getSingleResult()
        if result == None:
            return BigDecimal(0)
        else:
            return BigDecimal(result)
    
    def sumDebit(self, zpkId, statusDate):
        date = SimpleDateFormat('dd-MM-yyyy').parse(statusDate)
        sql = "Select sum(e.value) From DocumentPosition e Where e.debitZpk.id = :debitId and e.booked = 1 and e.bookingPeriod.defaultPeriod = 1 and e.createdAt <= :date"
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
        
    def obtainDescription(self, zpk):
        if zpk.getAccount() != None:
            return zpk.getAccount().getNumber()
        elif zpk.getPossession() != None:
            return zpk.getPossession().getFullAddress()
        elif zpk.getContractor() != None:
            return zpk.getContractor().getName()
        else:
            return ''
    
    def fillTemplate(self):
        self._context.put("community", self._community)
        self._context.put("statusDate", self._statusDate)
        self._context.put("zpks", self._zpks)
        self._context.put("labelDocumentCreationDate", self._label.get('report.documentCreationDate'))
        self._context.put("labelZpkStatus", self._label.get('report.zpkStatus'))
        self._context.put("labelStatusDate", self._label.get('report.statusDate'))
        self._context.put("labelCommunity", self._label.get('report.community'))
        self._context.put("labelAddress", self._label.get('report.address'))
        self._context.put("labelNumber", self._label.get('report.number'))
        self._context.put("labelCredit", self._label.get('report.credit'))
        self._context.put("labelDebit", self._label.get('report.debit'))
        self._context.put("labelDescription", self._label.get('report.description'))
        
        
    def getTemplateName(self):
        return "report-zpks-status"