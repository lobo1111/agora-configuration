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
        
    def getTemplateName(self):
        return "report-zpks-status"
    
   