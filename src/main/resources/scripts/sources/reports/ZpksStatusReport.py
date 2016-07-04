from reports.Report import Report

class ZpksStatusReport(Report):
    
    def obtainData(self):
        self._community = self.findById("Community", self._svars.get('communityId'))
        self._statusDate = self._svars.get('statusDate')
    
    def fillTemplate(self):
        self._context.put("community", self._community)
        self._context.put("statusDate", self._statusDate)
        
    def getTemplateName(self):
        return "report-zpks-status"
    
   