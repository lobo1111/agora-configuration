from pl.reaper.container.data import Contractor
from base.Container import Container
from entities.Zpk import ZpkManager

class ContractorManager(Container):
    
    def persist(self):
        pass

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
            