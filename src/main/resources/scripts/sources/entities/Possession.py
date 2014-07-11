from pl.reaper.container.data import Possession
from java.math import BigDecimal
from java.lang import Double
from java.lang import Integer
from base.Container import Container
from entities.Address import AddressManager
from entities.Community import CommunityManager
from entities.Element import ElementManager
from entities.Zpk import ZpkManager
from entities.Account import AccountManager

class PossessionManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
    
    def create(self):
        possession = Possession()
        self.setPossessionData(possession)
        self.setPossessionAdditionalData(possession)
        self.generateZpkNumber(possession)
        self.savePossession(possession)
        self.propagateElementsForNewPossession(possession)
        return possession;
        
    def update(self):
        possession = self.findPossessionById(self._svars.get('id'))
        self.setPossessionData(possession)
        self.setPossessionAdditionalData(possession)
        self.savePossession(possession)
        self.setElementsData(possession)
        return possession;
        
    def remove(self):
        possession = self.findPossessionById(self._svars.get('id'))
        self._entityManager.remove(possession.getAddress())
        for owner in possession.getOwners():
            self._entityManager.remove(owner)
        for possessionElement in possession.getElements():
            self._entityManager.remove(possessionElement)
        self._entityManager.remove(possession.getAdditionalData())
        self._entityManager.remove(possession)
        
    def generateZpkNumber(self, possession):
        manager = ZpkManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        zpkRent = manager.generateZpkForCommunity(possession.getCommunity(), "POSSESSION")
        zpkRent.setPossession(possession)
        possession.getZpks().add(zpkRent)
        zpkRepairFund = manager.generateZpkForCommunity(possession.getCommunity(), "POSSESSION_REPAIR_FUND")
        zpkRepairFund.setPossession(possession)
        possession.getZpks().add(zpkRepairFund)

    def propagateElementsForNewPossession(self, possession):
        manager = ElementManager()
        manager.setSvars(self._svars)
        manager.setEntityManager(self._entityManager)
        manager.propagateElementsForNewPossession(possession)
        
    def setElementsData(self, possession):
        notToRemove = []
        toRemove = []
        for i in range(int(self._svars.get(self._prefix + 'elementsCount'))): 
            self._svars.put("elementId", self._svars.get(self._prefix + str(i) + "_elementId"))
            self._svars.put("override", self._svars.get(self._prefix + str(i) + "_override"))
            self._svars.put("overrideValue", self._svars.get(self._prefix + str(i) + "_overrideValue"))
            manager = ElementManager()
            manager.setSvars(self._svars)
            manager.setEntityManager(self._entityManager)
            element = manager.CreateOrUpdatePossessionElement(possession)
            notToRemove.append(element.getId())
        for element in possession.getElements():
            if not (element.getId() in notToRemove):
                toRemove.append(element)
        for element in toRemove:
            possession.getElements().remove(element)
            self._entityManager.remove(element)
        
    def setPossessionData(self, possession):
        possession.setArea(BigDecimal(self._svars.get(self._prefix + 'possessionArea')))
        possession.setAddress(self.getAddress(possession))
        community = self.getCommunity(possession)
        possession.setCommunity(community)
        if possession.getId() == None or possession.getId() == 0:
            self._logger.info('New possession added to community')
            community.getPossessions().add(possession)
            self._entityManager.persist(community)
        
    def setPossessionAdditionalData(self, possession):
        possession.getAdditionalData().setPossession(possession)
        possession.getAdditionalData().setDeclaredArea(Double.parseDouble(self._svars.get(self._prefix + 'declaredArea')))
        possession.getAdditionalData().setDeclaredShare(Double.parseDouble(self._svars.get(self._prefix + 'declaredShare')))
        possession.getAdditionalData().setHotWater(Double.parseDouble(self._svars.get(self._prefix + 'hotWater')))
        possession.getAdditionalData().setColdWater(Double.parseDouble(self._svars.get(self._prefix + 'coldWater')))
        possession.getAdditionalData().setPeople(Integer.parseInt(self._svars.get(self._prefix + 'people')))
        possession.getAdditionalData().setRooms(Integer.parseInt(self._svars.get(self._prefix + 'rooms')))
#        if self._svars.get(self._prefix + 'account') != 0:
#            manager = AccountManager()
#            manager.setEntityManager(self._entityManager)
#            manager.setSvars(self._svars)
#            account = manager.findAccountById(self._svars.get(self._prefix + 'account'))
#            possession.getAdditionalData().setAccount(account)
        
    def getAddress(self, possession):
        addressManager = AddressManager()
        addressManager.setSvars(self._svars)
        addressManager.setEntityManager(self._entityManager)
        addressManager.setPrefix(self._prefix)
        return addressManager.getAddress(possession)

    def getCommunity(self, possession):
        communityManager = CommunityManager()
        communityManager.setSvars(self._svars)
        communityManager.setEntityManager(self._entityManager)
        return communityManager.findCommunityById(self._svars.get(self._prefix + 'communityId'))
        
    def savePossession(self, possession):
        self._logger.info(possession.longDescription())
        self._entityManager.persist(possession)
        communityManager = CommunityManager()
        communityManager.setSvars(self._svars)
        communityManager.setEntityManager(self._entityManager)
        communityManager.recalculateShares(possession.getCommunity().getId())
            
        
    def findAccountById(self, id):
        return self._entityManager.createQuery('Select a From Account a Where a.id = ' + id).getSingleResult()
        
    def findPossessionById(self, id):
        return self._entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()