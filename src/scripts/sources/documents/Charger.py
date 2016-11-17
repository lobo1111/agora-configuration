from java.text import SimpleDateFormat
from documents.Document import DocumentManager
from documents.helpers.Calculator import Calculator
from structures.Dictionary import DictionaryManager
from structures.BookingPeriod import BookingPeriodManager

class ChargerManager(DocumentManager):
    _calculator = Calculator()
    _type = "CHARGING"
    
    def remove(self):
        charging = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(charging)
    
    def alreadyCharged(self, possession):
        sql = "Select document "
        sql += " From Document document"
        sql += " Join document.positions pos"
        sql += " Join document.possession possession"
        sql += " Where possession.id = %d" % (possession.getId())
        sql += " and pos.month = %s" % (BookingPeriodManager().getCurrentMonth().getValue())
        sql += " and pos.bookingPeriod.defaultPeriod = true"
        sql += " and document.type = 'CHARGING'"
        result = self._entityManager.createQuery(sql).getResultList()
        return len(result) > 0
        
    def chargePossession(self, possession):
        if not self.alreadyCharged(possession) and possession.getElements().size() > 0:
            self._logger.info("Charging possession: %d" % possession.getId())
            self._svars.put("communityId", possession.getCommunity().getId())
            charging = self.initDocument(self._type)
            charging.setPossession(possession)
            charging.putAttribute("CREATE_DATE", str(SimpleDateFormat('dd-MM-yyyy').format(charging.getCreatedAt())))
            for possessionElement in possession.getElements():
                element = possessionElement.getElement()
                element.setGlobalValue(self.discoverValue(possessionElement))
                self._svars.put("value", str(self._calculator.calculate(element, possession)))
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
            self._logger.info("Already charged: %s" % str(self.alreadyCharged(possession)))
            self._logger.info("Elements: %d" % possession.getElements().size())
        
    def chargeCommunity(self, community):
        for possession in community.getPossessions():
            self.chargePossession(possession)
            
    def chargeAll(self):
        for possession in self.findAllActive():
            self.chargePossession(possession)
            
    def discoverValue(self, possessionElement):
        return possessionElement.calculateGlobalValue()
        
    def findAllActive(self):
        return self._entityManager.createQuery("Select p From Possession p Join p.community co Where co.inDate is not null and co.inDate <= CURRENT_DATE and co.outDate is null").getResultList()
     
    def isRepairFundElement(self, element):
        rfGroupId = DictionaryManager().findDictionaryInstance("PROPERTIES", "elements.repairFundGroup").getValue()
        self._logger.info("Repair Fund group: %d" % rfGroupId)
        elementGroupId = element.getGroup().getId()
        if rfGroupId == elementGroupId:
            self._logger.info("Element %s marked as repair fund related(%d)" % (element.getName(), elementGroupId))
            return True
        else:
            self._logger.info("Element %s marked as rent related(%d)" % (element.getName(), elementGroupId))
            return False