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
        obligation.setContractor(self.getContractor())
        obligation.setName(obligation.getContractor().getName())
        obligation.setCommunity(self.findCommunity(vars.get('communityId')))
        if vars.get('obligationGroupId') != '0':
            obligation.setObligationGroup(self.findObligationGroup(vars.get('obligationGroupId')))
        obligation.setZpk(self.createZpk(obligation))

    def getContractor(self):
        companyManager = CompanyManager()
        if vars.get('exsitingCompany') == 'true':
            return companyManager.findCompanyById(vars.get('obligationContractorId'))
        else:
            return companyManager.create()
        
    def findObligationById(self, id):
        return entityManager.createQuery('Select o From Obligation o Where o.id = ' + str(id)).getSingleResult()
    
    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)
    
    def findObligationGroup(self, id):
        return ObligationGroupManager().findObligationGroupById(id)

    def createZpk(self, obligation):
        zpk = ZpkManager().create()
        zpk.setObligation(obligation)
        return zpk