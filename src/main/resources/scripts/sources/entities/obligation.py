from pl.reaper.container.data import Obligation

class ObligationManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix

    def create(self):
        obligation = Obligation()
        self.setData(obligation)
        entityManager.persist(obligation)
        
    def update(self):
        obligation = self.findObligationById(vars.get(self._prefix + 'id'))
        self.setData(obligation)
        entityManager.persist(obligation)

    def remove(self):
        obligation = self.findObligationById(vars.get(self._prefix + 'id'))
        entityManager.remove(obligation.getZpk())
        entityManager.remove(obligation)
        
    def setData(self, obligation):
        obligation.setContractor(self.getContractor(obligation))
        obligation.setName(obligation.getContractor().getName())
        self._logger.info('com_get['+self._prefix + 'communityId'+']['+vars.get(self._prefix + 'communityId')+']')
        obligation.setCommunity(self.findCommunity(vars.get(self._prefix + 'communityId')))
        if vars.get(self._prefix + 'obligationGroupId') > '0':
            obligation.setObligationGroup(self.findObligationGroup(vars.get(self._prefix + 'obligationGroupId')))
        else:
            obligation.setObligationGroup(None)
        obligation.setZpk(self.createZpk(obligation))

    def getContractor(self, obligation):
        companyManager = CompanyManager()
        if vars.get(self._prefix + 'exsitingCompany') == 'true' and obligation.getContractor() != None and obligation.getContractor().getId() > 0:
            return companyManager.findCompanyById(vars.get(self._prefix + 'obligationContractorId'))
        else:
            return companyManager.create()
        
    def findObligationById(self, id):
        return entityManager.createQuery('Select o From Obligation o Where o.id = ' + str(id)).getSingleResult()
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)
    
    def findObligationGroup(self, id):
        return ObligationGroupManager().findObligationGroupById(id)

    def createZpk(self, obligation):
        zpkManager = ZpkManager()
        zpkManager.setPrefix(self._prefix)
        zpk = zpkManager.create()
        zpk.setObligation(obligation)
        return zpk