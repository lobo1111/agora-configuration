from pl.reaper.container.data import Obligation

class ObligationManager(Container):
    
    def create(self):
        obligation = Obligation()
        self.setData(obligation)
        entityManager.persist(obligation)
        
    def update(self):
        obligation = self.findObligationById(vars.get('id'))
        self.setData(obligation)
        entityManager.persist(obligation)
        
    def setData(self, obligation):
        obligation.setName(vars.get('obligationName'))
        obligation.setContractor(self.findContractor(vars.get('obligationContractorId')))
        obligation.setZpk(self.findContractorZpk(vars.get('obligationContractorZpkId')))
        obligation.setCommunity(self.findCommunity(vars.get('obligationCommunityId')))
        
    def findObligationById(self, id):
        return entityManager.createQuery('Select o From Obligation o Where o.id = ' + str(id)).getSingleResult()
    
    def findContractor(self, id):
        return CompanyManager().findCompanyById(id)
    
    def findContractorZpk(self, id):
        return ZpkManager().findZpkById(id)
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)