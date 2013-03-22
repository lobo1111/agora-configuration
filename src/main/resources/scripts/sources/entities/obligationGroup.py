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
        
    def findObligationGroupById(self, id):
        return entityManager.createQuery('Select o From ObligationGroup o Where o.id = ' + str(id)).getSingleResult()
    
    def findContractor(self, id):
        return CompanyManager().findCompanyById(id)
    
    def findContractorZpk(self, id):
        return ZpkManager().findZpkById(id)
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)