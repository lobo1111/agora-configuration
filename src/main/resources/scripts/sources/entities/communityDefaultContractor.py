from pl.reaper.container.data import CommunityDefaultContractor

class CommunityDefaultContractorManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        template = CommunityDefaultContractor()
        self.setTemplateData(template)
        self.saveTemplate(template)
        
    def update(self):
        template = self.findCommunityDefaultContractor(vars.get('id'))
        self.setTemplateData(template)
        self.saveTemplate(template)
        
    def remove(self):
        template = self.findCommunityDefaultContractor(vars.get('id'))
        entityManager.remove(template)
        entityManager.flush()
        
    def setTemplateData(self, template):
        template.setCompany(self.getCompany())
        template.setZpkNumber(vars.get('number'))
        template.setZpkDescription(vars.get('description'))
        
    def getCompany(self):
        companyManager = CompanyManager()
        return companyManager.findCompanyById(vars.get('companyId'))
    
    def saveTemplate(self, template):
        entityManager.persist(template)
        entityManager.flush()
        
    def findCommunityDefaultContractor(self, id):
        return entityManager.createQuery('Select a From CommunityDefaultContractor a Where a.id = ' + str(id)).getSingleResult()