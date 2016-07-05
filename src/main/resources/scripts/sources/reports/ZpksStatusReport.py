from reports.Report import Report
from java.text import SimpleDateFormat
from java.util import Date

class ZpksStatusReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._statusDate = self.getStatusDate()
        self._zpks = self.collectZpks(self._community.getZpks())
        
    def collectZpks(self, zpks):
        output = []
        for zpk in zpks:
            tmp = tmpZpk(zpk)
            output.append(tmp)
        return output
        
    def getStatusDate(self):
        if self._svars.get('statusDate') == '':
            return str(SimpleDateFormat('dd-MM-yyyy').format(Date()))
        else:
            return self._svars.get('statusDate')
    
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
    
class tmpZpk:
    _number = ''
    _debit = 0
    _credit = 0
    _description = ''
    
    def __init__(self, zpk):
        self._number = zpk.getType().getKey() + "-" + zpk.getNumber()
        self._debit = 0.0
        self._credit = 0.0
        self._decription = self.obtainDescription(zpk)
    
    def getNumber(self):
        return self._number
    
    def getDebit(self):
        return self._debit
    
    def getCredit(self):
        return self._credit
    
    def getDescription(self):
        return self._description
    
    def obtainDescription(self, zpk):
        if zpk.getAccount() != None:
            return zpk.getAccount().getNumber()
        elif zpk.getPossession() != None:
            return zpk.getPossession().getFullAddress()
        elif zpk.getContractor() != None:
            return zpk.getContractor().getName()
        else:
            return ''
    
    def addToCredit(self, amount):
        self._credit = self._credit + amount
        
    def addToDebit(self, amount):
        self._debit = self._debit + amount