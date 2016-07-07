from reports.Report import Report
from java.text import SimpleDateFormat
from java.math import BigDecimal
from java.math import RoundingMode
from structures.BookingPeriod import BookingPeriodManager
from structures.Account import AccountManager

class ChargingPredictionReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._possession = self.findById("Possession", self._svars.get('possessionId'))
        self._total = BigDecimal(0)
        self._items = self.collectItems()
        self._paymentStartDate = self.getPaymentStartDate()
        self._chargingAccount = self.getChargingAccount()
        self._rfAccount = self.getRFAccount()
        
    def collectItems(self):
        output = []
        elements = self._possession.getElements()
        elements = sorted(elements, key=lambda item: item.getGroup().getValue() + item.getName())
        lastGroupId = elements[0].getGroup().getId()
        groupTotal = BigDecimal(0)
        groupItems = 0
        for element in elements:
            if element.getGroup().getId() != lastGroupId:
                if groupItems > 1:
                    self.createTotalLine(output, groupTotal)
                    groupTotal = BigDecimal(0)
                self.createEmptyLine(output)
                groupItems = 0
                lastGroupId = element.getGroup().getId()
            item = dict([])
            item['group'] = element.getGroup().getValue()
            item['element'] = element.getName()
            item['value'] = self.calculateValue(element)
            groupItems += 1
            output.append(item)
        self.createTotalLine(output, groupTotal)
        self.createEmptyLine(output)
        self.createTotalLine(output, self._total)
        return output
    
    def createTotalLine(self, output, total):
        item = dict([])
        item['group'] = ''
        item['element'] = self._label.get('report.totalValue')
        item['value'] = total
        output.append(item)
    
    def createEmptyLine(self, output):
        item = dict([])
        item['group'] = ' '
        item['element'] = ' '
        item['value'] = ' '
        output.append(item)
    
    def calculateValue(self, element):
        return BigDecimal(0)
    
    def getPaymentStartDate(self):
        bp = BookingPeriodManager()
        return self._label.get(bp.getCurrentMonthLabel()) + " " + bp.findDefaultBookingPeriod().getName()
    
    def getChargingAccount(self):
        for account in self._community.getAccounts():
            if account.getType().getKey() in ["DEFAULT", "RENT"]:
                return AccountManager().makeReadable(account.getNumber())
    
    def getRFAccount(self):
        for account in self._community.getAccounts():
            if account.getType().getKey() in ["REPAIR_FUND"]:
                return AccountManager().makeReadable(account.getNumber())
    
    def fillTemplate(self):
        self._context.put("paymentStartDate", self._paymentStartDate)
        self._context.put("totalValue", self._total)
        self._context.put("chargingAccount", self._chargingAccount)
        self._context.put("rfAccount", self._rfAccount)
        self._context.put("community", self._community)
        self._context.put("possession", self._possession)
        self._context.put("items", self._items)
        self._context.put("labelDocumentCreationDate", self._label.get('report.documentCreationDate'))
        self._context.put("labelChargingPrediction", self._label.get('report.chargingPrediction'))
        self._context.put("labelCommunity", self._label.get('report.community'))
        self._context.put("labelPossession", self._label.get('report.possession'))
        self._context.put("labelOwners", self._label.get('report.owners'))
        self._context.put("labelPaymentStartDate", self._label.get('report.paymentStartDate'))
        self._context.put("labelGroup", self._label.get('report.group'))
        self._context.put("labelElement", self._label.get('report.element'))
        self._context.put("labelValue", self._label.get('report.value'))
        self._context.put("labelTotal", self._label.get('report.totalValue'))
        self._context.put("labelChargingAccount", self._label.get('report.chargingAccount'))
        self._context.put("labelRFAccount", self._label.get('report.rfAccount'))
        
        
    def getTemplateName(self):
        return "report-charging-prediction"