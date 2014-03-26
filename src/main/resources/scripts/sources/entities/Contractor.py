from pl.reaper.container.data import Contractor
from base.Container import Container
from entities.Company import CompanyManager
from entities.Community import CommunityManager
from entities.Zpk import ZpkManager

class ContractorManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix

    def create(self):
        obligation = Contractor()
        self.setData(obligation)
        self.generateZpkNumber(obligation)
        entityManager.persist(obligation)
        entityManager.flush()
        return obligation
        
    def update(self):
        obligation = self.findContractorById(svars.get(self._prefix + 'id'))
        self.setData(obligation)
        entityManager.persist(obligation)
        return obligation

    def remove(self):
        obligation = self.findContractorById(svars.get(self._prefix + 'id'))
        entityManager.remove(obligation.getZpk())
        entityManager.remove(obligation)
        
    def setData(self, obligation):
        obligation.setCompany(self.getCompany(obligation))
        obligation.setName(obligation.getCompany().getName())
        obligation.setCommunity(self.findCommunity(svars.get(self._prefix + 'communityId')))

    def generateZpkNumber(self, obligation):
        manager = ZpkManager()
        zpkContractor = manager.generateZpkForCommunity(obligation.getCommunity(), "CONTRACTOR")
        zpkContractor.setContractor(obligation)
        obligation.getZpks().add(zpkContractor)
        zpkCost = manager.generateZpkForCommunity(obligation.getCommunity(), "CONTRACTOR_COST")
        zpkCost.setContractor(obligation)
        obligation.getZpks().add(zpkCost)

    def getCompany(self, obligation):
        companyManager = CompanyManager()
        companyManager.setPrefix(self._prefix)
        if svars.get(self._prefix + 'exsitingCompany') == 'true':
            return companyManager.findCompanyById(svars.get(self._prefix + 'obligationCompanyId'))
        else:
            return companyManager.create()
        
    def findContractorById(self, id):
        return entityManager.createQuery('Select o From Contractor o Where o.id = ' + str(id)).getSingleResult()
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)
    