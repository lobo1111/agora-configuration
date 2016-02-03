from pl.reaper.container.data import Contractor
from base.Container import Container
from structures.Zpk import ZpkManager
from structures.Company import CompanyManager

class ContractorManager(Container):
    
    def persist(self):
        company = CompanyManager().findOrCreate()
        CompanyManager().setData(company)
        contractor = self.getOrCreateContractor(company)
        return self.saveEntity(contractor)
    
    def remove(self):
        contractor = self.findById("Contractor", self._svars.get('id'))
        contractor.setDisabled(True)
        self.saveEntity(contractor)

    def createDefaultContractorsForCommunity(self, community):
        for company in self.collectDefaultCompanies():
            contractor = Contractor()
            contractor.setCompany(company)
            contractor.setCommunity(community)
            community.getContractors().add(contractor)
            ZpkManager().createZpksForContractor(contractor)
            
    def collectDefaultCompanies(self):
        sql = 'Select c From Company c Where c.defaultContractor = true'
        return self._entityManager.createQuery(sql).getResultList()
    
    def getOrCreateContractor(self, company):
        contractor = self.findContractor(company.getContractors())
        if contractor == None:
            self._logger.info("Contractor not found for company(%s) and community(%d), creating new one..." % (company.getName(), int(self._svars.get('communityId'))))
            contractor = Contractor()
            contractor.setCommunity(self.findById("Community", int(self._svars.get('communityId'))))
        self.setData(contractor, company)
        return contractor
    
    def setData(self, contractor, company):
        contractor.setCompany(company)
        contractor.setName(company.getName())
    
    def findContractor(self, contractors):
        for contractor in contractors:
            if not contractor.isDisabled() and contractor.getCommunity().getId() == int(self._svars.get('communityId')):
                return contractor