from pl.reaper.container.data import Contractor

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
        obligation = self.findContractorById(vars.get(self._prefix + 'id'))
        self.setData(obligation)
        entityManager.persist(obligation)
        return obligation

    def remove(self):
        obligation = self.findContractorById(vars.get(self._prefix + 'id'))
        entityManager.remove(obligation.getZpk())
        entityManager.remove(obligation)
        
    def setData(self, obligation):
        obligation.setContractor(self.getContractor(obligation))
        obligation.setName(obligation.getContractor().getName())
        obligation.setCommunity(self.findCommunity(vars.get(self._prefix + 'communityId')))

    def generateZpkNumber(self, obligation):
        manager = ZpkManager()
        zpkContractor = manager.generateZpkForCommunity(obligation.getCommunity(), "CONTRACTOR")
        zpkContractor.setContractor(obligation)
        obligation.getZpks().add(zpkContractor)
        zpkCost = manager.generateZpkForCommunity(obligation.getCommunity(), "CONTRACTOR_COST")
        zpkCost.setContractor(obligation)
        obligation.getZpks().add(zpkCost)

    def getContractor(self, obligation):
        companyManager = CompanyManager()
        companyManager.setPrefix(self._prefix)
        if vars.get(self._prefix + 'exsitingCompany') == 'true' and obligation.getContractor() != None and obligation.getContractor().getId() > 0:
            return companyManager.findCompanyById(vars.get(self._prefix + 'obligationContractorId'))
        else:
            return companyManager.create()
        
    def findContractorById(self, id):
        return entityManager.createQuery('Select o From Contractor o Where o.id = ' + str(id)).getSingleResult()
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)
    