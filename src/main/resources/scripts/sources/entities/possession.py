from pl.reaper.container.data import Person
from pl.reaper.container.data import Possession
from java.math import BigDecimal

class PossessionManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        possession = Possession()
        self.setPossessionData(possession)
        self.savePossession(possession)
        
    def update(self):
        possession = self.findPossessionById(vars.get('id'))
        self.setPossessionData(possession)
        self.savePossession(possession)
        
    def setPossessionData(self, possession):
        possession.setArea(BigDecimal(vars.get('possessionArea')))
        possession.setAddress(self.getAddress(possession))
        possession.setCommunity(self.getCommunity(possession))
        
    def getAddress(self, possession):
        addressManager = AddressManager()
        return addressManager.getAddress(possession)

    def getCommunity(self, possession):
        communityManager = CommunityManager()
        return communityManager.findCommunityById(vars.get('communityId'))
        
    def savePossession(self, possession):
        self._logger.info(possession.longDescription())
        entityManager.persist(possession)
        CommunityManager().recalculateShares(possession.getCommunity().getId())
        
    def findPossessionById(self, id):
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()