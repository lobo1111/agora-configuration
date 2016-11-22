from reports.Report import Report
from structures.Dictionary import DictionaryManager
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
        counter = 0
        for document in self.getQuery().getResultList():
            if document not in processed:
                item = dict([])
                item['no'] = counter
                item['root'] = True
                counter += 1
                item['type'] = self.getType(document)
                item['date'] = self.getCreateDate(document)
                item['value'] = self.calculateValue(document)
                item['balance'] = item['value'].add(self._startBalance)
                output.append(item)
                rent, rf = self.getSubItems(document)
                rent['no'] = counter
                counter += 1
                rf['no'] = counter
                counter += 1
                output.append(rent)
                output.append(rf)
                processed.append(document)
        output = sorted(output, key=lambda item: item['no'], reverse=True)
        s = 1
        while s < len(output) and output[s]['root'] == False:
            s += 1
        for i in range(s, len(output)):
            if output[i]['root']:
                j = 1
                while output[j]['root'] == False:
                    j += 1
                output[i]['balance'] = output[i - j]['balance'].add(output[i]['value'])
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


    def getSubItems(self, document):
        rfGroupId = int(DictionaryManager().findDictionaryInstance("PROPERTIES", "elements.repairFundGroup").getValue())
        rf = dict([])
        rent = dict([])
        rf['root'] = rent['root'] = False
        rf['date'] = rent['date'] = ' '
        rf['balance'] = rent['balance'] = ' '
        rf['type'] = self._label.get('report.repairFund')
        rent['type'] = self._label.get('report.rent')
        valueRent = BigDecimal(0)
        valueRf = BigDecimal(0)
        for position in document.getPositions():
            if document.getType() == "CHARGING":
                if int(position.getAttribute("ELEMENT_GROUP_ID").getValue()) == rfGroupId:
                    valueRf = valueRf.add(position.getValue().multiply(BigDecimal(-1)))
                else:
                    valueRent = valueRent.add(position.getValue().multiply(BigDecimal(-1)))
            else:
                if position.getType() == "POSSESSION_PAYMENT_RENT":
                    valueRent = valueRent.add(position.getValue())
                else:
                    valueRf = valueRf.add(position.getValue())
        rent['value'] = valueRent
        rf['value'] = valueRf
        return rent, rf
    
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
        self._context.put("labelCreatedAt", self._label.get('report.operationDate'))
        self._context.put("labelValue", self._label.get('report.value'))
        self._context.put("labelType", self._label.get('report.documentType'))
        
    def getTemplateName(self):
        return "report-chargings"