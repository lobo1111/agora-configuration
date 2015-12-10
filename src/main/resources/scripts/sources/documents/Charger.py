from document.Document import Document
from document.Document.helpers.Calculator import Calculator
from entities.BookingPeriod import BookingPeriodManager
from entities.Dictionary import DictionaryManager
from pl.reaper.container.data import Charging
from pl.reaper.container.data import ChargingPosition

class Charger(Document):
    self._calculator = Calculator()
    
    def remove(self):
        charging = self.findById("Charging", self._svars.get('id'))
        self.cancelDocument(charging)
    
    def chargeAll(self):
        self._queue = ChargingQueueManager()
        self._bookingPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        item = self._queue.popFromQueue()
        while not item is None:
            self._logger.info('charging: %s' % item.getType())
            self.charge(item)
            item = self._queue.popFromQueue()
        
    def alreadyCharged(self, possession):
        try:
            self._entityManager.createQuery("Select p From Charging c Join c.possession p Where p.id = " + str(possession.getId()) + " and c.month = %s)" % self._currentMonth).getSingleResult()
            return True
        except:
            return False
        
    def charge(self, item):
        if item.getType().toString() == "ALL":
            self.chargeAllUncharged()
        elif item.getType().toString() == "COMMUNITY":
            self.chargeCommunity(item.getCommunity())
        elif item.getType().toString() == "POSSESSION":
            self.chargePossession(item.getPossession())
            
    def chargePossession(self, possession):
        if not self.alreadyCharged(possession) and possession.getElements().size() > 0:
            charging = self.initDocument(Charging(), Charging.TYPE)
            charging.setPossession(possession)
            for possessionElement in possession.getElements():
                element = possessionElement.getElement()
                element.setGlobalValue(self.discoverValue(possessionElement))
                chargingPosition = self.initPosition(charging, ChargingPosition())
                chargingPosition.setDescription(element)
                chargingPosition.setGroup(element.getGroup())
                chargingPosition.setValue(self._calculator.calculate(element, possession))
                if self.isRepairFundElement(element):
                    chargingPosition.setCreditZpk(self.findZpk(charging.getCommunity().getZpks(), 'CHARGING_RENT'))
                    chargingPosition.setDebitZpk(self.findZpk(possession.getZpks(), 'POSSESSION'))
                else:
                    chargingPosition.setCreditZpk(self.findZpk(charging.getCommunity().getZpks(), 'CHARGING_REPAIR_FUND'))
                    chargingPosition.setDebitZpk(self.findZpk(possession.getZpks(), 'POSSESSION_REPAIR_FUND'))
            return self.saveDocument(charging)
            
   def chargeCommunity(self, community):
        for possession in community.getPossessions():
            self.chargePossession(possession)
            
    def chargeAllUncharged(self):
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
        return self._entityManager.createQuery("Select p From Possession p Join p.community co Where co.inDate <= CURRENT_DATE AND p.id not in(Select ped.id From Charging c Join c.bookingPeriod bp Join c.possession ped Where bp.defaultPeriod = 1 AND c.month = %s) and p.community.outDate is null" % self._currentMonth).getResultList()
     
    def isRepairFundElement(self, element):
        return DictionaryManager.findDictionaryInstance("PROPERTIES", "elements.repairFundGroup").getValue() == element.getGroup().getId()