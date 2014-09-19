from pl.reaper.container.data import Contractor
from base.Container import Container
from entities.Company import CompanyManager
from entities.Zpk import ZpkManager

class ContractorManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix

    def create(self):
        obligation = Contractor()
        self.setData(obligation)
        self.generateZpkNumber(obligation)
        self._entityManager.persist(obligation)
        self._entityManager.flush()
        return obligation
        
    def update(self):
        obligation = self.findContractorById(self._svars.get(self._prefix + 'id'))
        self.setData(obligation)
        self._entityManager.persist(obligation)
        return obligation

    def remove(self):
        obligation = self.findContractorById(self._svars.get(self._prefix + 'id'))
        self._entityManager.remove(obligation.getZpk())
        self._entityManager.remove(obligation)
        
    def setData(self, obligation):
        obligation.setCompany(self.getCompany(obligation))
        obligation.setName(obligation.getCompany().getName())
        obligation.setCommunity(self.findCommunity(self._svars.get(self._prefix + 'communityId')))

    def generateZpkNumber(self, obligation):
        manager = ZpkManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        zpkContractor = manager.generateZpkForCommunity(obligation.getCommunity(), "CONTRACTOR")
        manager.setStartBalance(zpkContractor, float(self._svars.get('startCredit2')), float(self._svars.get('startDebit2')))
        zpkContractor.setContractor(obligation)
        obligation.getZpks().add(zpkContractor)
        zpkCost = manager.generateZpkForCommunity(obligation.getCommunity(), "CONTRACTOR_COST")
        manager.setStartBalance(zpkCost, float(self._svars.get('startCredit5')), float(self._svars.get('startDebit5')))
        zpkCost.setContractor(obligation)
        obligation.getZpks().add(zpkCost)

    def getCompany(self, obligation):
        return CompanyManager().findCompanyById(self._svars.get(self._prefix + 'obligationContractorId'))
        
    def findContractorById(self, id):
        return self._entityManager.createQuery('Select o From Contractor o Where o.id = ' + str(id)).getSingleResult()
    
    def findCommunity(self, id):
        from entities.Community import CommunityManager
        manager = CommunityManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        return manager.findCommunityById(id)
    