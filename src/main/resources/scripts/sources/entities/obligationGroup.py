from pl.reaper.container.data import ObligationGroup

class ObligationGroupManager(Container):

    def create(self):
        obligation = ObligationGroup()
        self.setData(obligation)
        entityManager.persist(obligation)
        
    def update(self):
        obligation = self.findObligationGroupById(vars.get('id'))
        self.setData(obligation)
        entityManager.persist(obligation)
        
    def setData(self, obligation):
        obligation.setName(vars.get('obligationGroupName'))
        obligation.setCommunity(self.findCommunity(vars.get('obligationGroupCommunityId')))
        self.setZpks(obligation, vars.get('boundedZpksCount'))
        self.setObligations(obligation, vars.get('boundedObligationsCount'))
        
    def setZpks(self, group, counter):
        group.getZpks().clear()
        for i in range(int(counter)):
            zpkId = int(vars.get('boundedZpk' + str(i)))
            zpk = self.findZpk(zpkId)
            group.getZpks().add(zpk)
        
    def setObligations(self, group, counter):
        group.getObligations().clear()
        for i in range(int(counter)):
            obligationId = int(vars.get('boundedObligation' + str(i)))
            obligation = self.findObligation(obligationId)
            group.getObligations().add(obligation)
        
    def findObligationGroupById(self, id):
        return entityManager.createQuery('Select o From ObligationGroup o Where o.id = ' + str(id)).getSingleResult()
    
    def findContractor(self, id):
        return CompanyManager().findCompanyById(id)
    
    def findContractorZpk(self, id):
        return ZpkManager().findZpkById(id)
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)
    
    def findZpk(self, id):
        return ZpkManager().findZpkById(id)
    
    def findObligation(self, id):
        return ObligationManager().findObligationById(id)