from reports.Report import Report
from java.text import SimpleDateFormat
from java.math import BigDecimal
from java.math import RoundingMode

class ChargingsReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._possession = self.findById("Possession", self._svars.get('possessionId'))
        self._startBalance = self.getStartBalance()
        self._transactions = self.collectTransactions()
        
    def getStartBalance(self):
        balance = BigDecimal(0)
        for zpk in self._possession.getZpks():
            balance = balance.add(BigDecimal(zpk.getCurrentBalance().getStartCredit() - zpk.getCurrentBalance().getStartDebit()).setScale(2, RoundingMode.HALF_UP))
        return balance
        
    def collectTransactions(self):
        processed = []
        output = []
        for document in self.getQuery().getResultList():
            if document not in processed:
                item = dict([])
                item['type'] = self.getType(document)
                item['date'] = self.getCreateDate(document)
                item['value'] = self.calculateValue(document)
                item['balance'] = item['value'].add(self._startBalance)
                output.append(item)
                processed.append(document)
        output = sorted(output, key=lambda item: SimpleDateFormat('dd-MM-yyyy').parse(item['date']).getTime())
        for i in range(1, len(output)):
            output[i]['balance'] = output[i - 1]['balance'].add(output[i]['value'])
        return output
    
    def getCreateDate(self, document):
        if document.getAttribute("CREATE_DATE") != None:
            return document.getAttribute("CREATE_DATE").getValue()
        for position in document.getPositions():
            if position.getAttribute("CREATE_DATE") != None:
                return position.getAttribute("CREATE_DATE").getValue()
        return str(SimpleDateFormat('dd-MM-yyyy').format(document.getCreatedAt()))
    
    def getType(self, document):
        if document.getType() == "BANK_NOTE":
            return self._label.get('document.bankNote')
        elif document.getType() == "POSSESSION_PAYMENT":
            return self._label.get('document.possessionPayment')
        elif document.getType() == "CHARGING":
            return self._label.get('document.charging')
        else:
            return document.getType()
    
    def calculateValue(self, document):
        value = BigDecimal(0)
        for position in document.getPositions():
            if document.getType() == "CHARGING":
                value = value.add(position.getValue().multiply(BigDecimal(-1)))
            else:
                value = value.add(position.getValue())
        return value
    
    def getQuery(self):
        sql = "Select d From Document d Join d.positions p Join p.bookingPeriod bp Where d.possession.id = :pid And bp.defaultPeriod = 1"
        query = self._entityManager.createQuery(sql)
        query.setParameter("pid", self._possession.getId())
        return query
    
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
        self._context.put("labelType", self._label.get('report.documentType'))
        
    def getTemplateName(self):
        return "report-chargings"