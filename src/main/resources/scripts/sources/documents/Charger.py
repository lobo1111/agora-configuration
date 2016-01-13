from java.text import SimpleDateFormat
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
        sql = "Select document "
        sql += " From Document document"
        sql += " Join document.positions position"
        sql += " Join document.possession possession"
        sql += " Where possession.id = %d" % (possession.getId())
        sql += " and position.month = %s" % (BookingPeriodManager().getCurrentMonth())
        sql += " and position.bookingPeriod.defaultPeriod = true"
        result = self._entityManager.createQuery(sql).getResultList()
        return len(result) > 0
        
    def chargePossession(self, possession):
        if not self.alreadyCharged(possession) and possession.getElements().size() > 0:
            self._svars.put("communityId", possession.getCommunity().getId())
            charging = self.initDocument(self._type)
            charging.setPossession(possession)
            charging.putAttribute("CREATE_DATE", str(SimpleDateFormat('dd-MM-yyyy').format(charging.getCreatedAt())))
            for possessionElement in possession.getElements():
                element = possessionElement.getElement()
                element.setGlobalValue(self.discoverValue(possessionElement))
                self._svars.put("value", self._calculator.calculate(element, possession))
                chargingPosition = self.initPosition(charging)
                chargingPosition.setDescription(possessionElement.getElement().getName())
                chargingPosition.putAttribute("ELEMENT_GROUP_ID", str(possessionElement.getElement().getGroup().getId()))
                chargingPosition.putAttribute("ELEMENT_GROUP_NAME", str(possessionElement.getElement().getGroup().getValue()))
                if self.isRepairFundElement(element):
                    chargingPosition.setCreditZpk(self.findZpk(charging.getCommunity().getZpks(), 'CHARGING_RENT'))
                    chargingPosition.setDebitZpk(self.findZpk(possession.getZpks(), 'POSSESSION'))
                else:
                    chargingPosition.setCreditZpk(self.findZpk(charging.getCommunity().getZpks(), 'CHARGING_REPAIR_FUND'))
                    chargingPosition.setDebitZpk(self.findZpk(possession.getZpks(), 'POSSESSION_REPAIR_FUND'))
                self.bound(charging, chargingPosition)
            return self.saveDocument(charging)
        else:
            self._logger.info("Possession %d omitted, reason:" % possession.getId())
            self._logger.info("Already charted: %s" % str(self.alreadyCharged(possession)))
            self._logger.info("Elements: %d" % possession.getElements().size())
        
    def chargeCommunity(self, community):
        for possession in community.getPossessions():
            self.chargePossession(possession)
            
    def chargeAll(self):
        for possession in self.findAllActive():
            self.chargePossession(possession)
            
    def discoverValue(self, possessionElement):
        if possessionElement.isOverrideParentValue():
            return possessionElement.getGlobalValue()
        elif possessionElement.getElementCommunity() != None and possessionElement.getElementCommunity().isOverrideParentValue():
            return possessionElement.getElementCommunity().getGlobalValue()
        else:
            return possessionElement.getElement().getGlobalValue()
        
    def findAllActive(self):
        return self._entityManager.createQuery("Select p From Possession p Join p.community co Where (co.inDate <= CURRENT_DATE or co.inDate is null) and p.community.outDate is null").getResultList()
     
    def isRepairFundElement(self, element):
        return DictionaryManager().findDictionaryInstance("PROPERTIES", "elements.repairFundGroup").getValue() == element.getGroup().getId()