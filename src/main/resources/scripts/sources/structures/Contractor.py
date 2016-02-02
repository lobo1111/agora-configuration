from pl.reaper.container.data import Company
from pl.reaper.container.data import Contractor
from base.Container import Container
from entities.Zpk import ZpkManager
from structures.Company import CompanyManager

class ContractorManager(Container):
    
    def persist(self):
        company = self.initStructure()
        CompanyManager().setData(company)
        if not self.contractorExists(company):
            contractor = self.createContractor(company)
        return self.saveEntity(contractor)

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
    
    def createContractor(self, company):
        for contractor in company.getContractors():
            if contractor.getCommunity().getId() == int(self._svars.get('communityId')):
                self._logger.info("Contractor found for company(%d) and community(%d)" % (company.getId(), int(self._svars.get('communityId'))))
                return contractor
        self._logger.info("Contractor not found for company(%d) and community(%d), creating new one..." % (company.getId(), int(self._svars.get('communityId'))))
        contractor = Contractor()
        contractor.setCommunity(self.findById("Community", int(self._svars.get('communityId'))))
        contractor.setCompany(company)
        return contractor
    
    def initStructure(self):
        if self._svars.get('id') != '0':
            self._logger.info("Company persist - it's an update. Found id: %s" % self._svars.get('id'))
            return self.findById("Company", int(self._svars.get('id')))
        else:
            self._logger.info("Company persist - it's a new structure")
            return Company()
            