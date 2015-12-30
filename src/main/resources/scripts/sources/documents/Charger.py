from documents.Document import DocumentManager
from documents.helpers.Calculator import Calculator
from entities.Dictionary import DictionaryManager
from entities.BookingPeriod import BookingPeriodManager

class ChargerManager(DocumentManager):
    _calculator = Calculator()
    _type = "CHARGING"
    
    def remove(self):
        charging = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(charging)
    
    def alreadyCharged(self, possession):
        try:
            self._entityManager.createQuery("Select p From Charging c Join c.possession p Where p.id = " + str(possession.getId()) + " and c.month = %s)" % BookingPeriodManager().getCurrentMonth()).getSingleResult()
            return True
        except:
            return False
        
    def chargePossession(self, possession):
        if not self.alreadyCharged(possession) and possession.getElements().size() > 0:
            self._svars.put("communityId", possession.getCommunity().getId())
            charging = self.initDocument(self._type)
            charging.setCommunity(possession.getCommunity())
            charging.setPossession(possession)
            for possessionElement in possession.getElements():
                element = possessionElement.getElement()
                element.setGlobalValue(self.discoverValue(possessionElement))
                chargingPosition = self.initPosition(charging)
                chargingPosition.setDescription(possessionElement.getElement().getName())
                chargingPosition.putAttribute("ELEMENT_KEY", possessionElement.getElement().getKey())
                chargingPosition.putAttribute("ELEMENT_GROUP_ID", possessionElement.getElement().getGroup().getId())
                chargingPosition.putAttribute("ELEMENT_GROUP_Name", possessionElement.getElement().getGroup().getValue())
                chargingPosition.setValue(self._calculator.calculate(element, possession))
                if self.isRepairFundElement(element):
                    chargingPosition.setCreditZpk(self.findZpk(charging.getCommunity().getZpks(), 'CHARGING_RENT'))
                    chargingPosition.setDebitZpk(self.findZpk(possession.getZpks(), 'POSSESSION'))
                else:
                    chargingPosition.setCreditZpk(self.findZpk(charging.getCommunity().getZpks(), 'CHARGING_REPAIR_FUND'))
                    chargingPosition.setDebitZpk(self.findZpk(possession.getZpks(), 'POSSESSION_REPAIR_FUND'))
                self.bound(charging, chargingPosition)
            return self.saveDocument(charging)
        
    def chargeCommunity(self, community):
        for possession in community.getPossessions():
            self.chargePossession(possession)
            
    def chargeAll(self):
        for possession in self.findAllUncharged():
            self.chargePossession(possession)
            
    def discoverValue(self, possessionElement):
        if possessionElement.isOverrideParentValue():
            return possessionElement.getGlobalValue()
        elif possessionElement.getElementCommunity() != None and possessionElement.getElementCommunity().isOverrideParentValue():
            return possessionElement.getElementCommunity().getGlobalValue()
        else:
            return possessionElement.getElement().getGlobalValue()
        
    def findAllUncharged(self):
        return self._entityManager.createQuery("Select p From Possession p Join p.community co Where co.inDate <= CURRENT_DATE AND p.id not in(Select ped.id From Charging c Join c.bookingPeriod bp Join c.possession ped Where bp.defaultPeriod = 1 AND c.month = %s) and p.community.outDate is null" % BookingPeriodManager().getCurrentMonth()).getResultList()
     
    def isRepairFundElement(self, element):
        return DictionaryManager.findDictionaryInstance("PROPERTIES", "elements.repairFundGroup").getValue() == element.getGroup().getId()