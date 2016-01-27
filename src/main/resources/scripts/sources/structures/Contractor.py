from pl.reaper.container.data import Contractor
from base.Container import Container
from entities.Zpk import ZpkManager

class ContractorManager(Container):

    def createDefaultContractorsForCommunity(self, community):
        for company in self.collectDefaultCompanies():
            contractor = Contractor()
            contractor.setCompany(company)
            contractor.setCommunity(community)
            community.getContractors().add(contractor)
            ZpkManager().createZpksForContractor(contractor)
            