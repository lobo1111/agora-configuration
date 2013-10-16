from pl.reaper.container.data import Person
from pl.reaper.container.data import Possession
from pl.reaper.container.data import PossessionAutoPaymentOrder
from java.math import BigDecimal
from java.lang import Double
from java.lang import Integer

class PossessionManager(Container):
    _logger = Logger([:_scriptId])
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
    
    def create(self):
        possession = Possession()
        self.setPossessionData(possession)
        self.setPossessionAdditionalData(possession)
        self.savePossession(possession)
        self.generateZpkNumber(possession)
        self.propagateElementsForNewPossession(possession)
        return possession;
        
    def update(self):
        possession = self.findPossessionById(vars.get('id'))
        self.setPossessionData(possession)
        self.setPossessionAdditionalData(possession)
        self.savePossession(possession)
        self.setElementsData(possession)
        return possession;
        
    def remove(self):
        possession = self.findPossessionById(vars.get('id'))
        entityManager.remove(possession.getAddress())
        for owner in possession.getOwners():
            entityManager.remove(owner)
        for possessionElement in possession.getElements():
            entityManager.remove(possessionElement)
        entityManager.remove(possession.getAdditionalData())
        entityManager.remove(possession)
        
    def generateZpkNumber(self, possession):
        zpk = ZpkManager().generateZpkForPossession(possession)
        possession.setZpk(zpk)
        entityManager.persist(possession)
        
    def propagateElementsForNewPossession(self, possession):
        manager = ElementManager()
        manager.propagateElementsForNewPossession(possession)
        
    def setElementsData(self, possession):
        for i in range(int(vars.get(self._prefix + 'elementsCount'))): 
            vars.put("elementId", vars.get(self._prefix + str(i) + "_elementId"))
            vars.put("override", vars.get(self._prefix + str(i) + "_override"))
            vars.put("overrideValue", vars.get(self._prefix + str(i) + "_overrideValue"))
            manager = ElementManager()
            manager.CreateOrUpdatePossessionElement(possession)
        
    def setPossessionData(self, possession):
        possession.setArea(BigDecimal(vars.get(self._prefix + 'possessionArea')))
        possession.setAddress(self.getAddress(possession))
        community = self.getCommunity(possession)
        possession.setCommunity(community)
        if possession.getId() == 0:
            community.getPossessions().add(possession)
        
    def setPossessionAdditionalData(self, possession):
        possession.getAdditionalData().setPossession(possession)
        possession.getAdditionalData().setDeclaredArea(Double.parseDouble(vars.get(self._prefix + 'declaredArea')))
        possession.getAdditionalData().setDeclaredShare(Double.parseDouble(vars.get(self._prefix + 'declaredShare')))
        possession.getAdditionalData().setHotWater(Double.parseDouble(vars.get(self._prefix + 'hotWater')))
        possession.getAdditionalData().setColdWater(Double.parseDouble(vars.get(self._prefix + 'coldWater')))
        possession.getAdditionalData().setPeople(Integer.parseInt(vars.get(self._prefix + 'people')))
        possession.getAdditionalData().setRooms(Integer.parseInt(vars.get(self._prefix + 'rooms')))
        
    def getAddress(self, possession):
        addressManager = AddressManager()
        addressManager.setPrefix(self._prefix)
        return addressManager.getAddress(possession)

    def getCommunity(self, possession):
        communityManager = CommunityManager()
        return communityManager.findCommunityById(vars.get(self._prefix + 'communityId'))
        
    def savePossession(self, possession):
        self._logger.info(possession.longDescription())
        entityManager.persist(possession)
        CommunityManager().recalculateShares(possession.getCommunity().getId())
        
    def findAccountById(self, id):
        return entityManager.createQuery('Select a From Account a Where a.id = ' + id).getSingleResult()
        
    def findPossessionById(self, id):
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()