from reports.Report import Report

class ZpksStatusReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._statusDate = self._svars.get('statusDate')
        self._zpks = self._community.getZpks()
    
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
    
   