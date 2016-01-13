from actions.helpers.Restriction import Restriction
from entities.BookingPeriod import BookingPeriodManager

class ChargingRestriction(Restriction):
    
    def calculate(self):
        activePossessions = self.countActivePossessions()
        createdChargings = self.countChargings()
        if activePossessions == createdChargings:
           self._result = True
        else:
            self._message = "Brakuje %d naliczen" % (activePossessions - createdChargings)
            self._result = False
        
    def countActivePossessions(self):
        sql = "Select count(possession) From Possession possession Join possession.community community Where community.outDate is Null"
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def countChargings(self):
        currentMonth = BookingPeriodManager().getCurrentMonth()
        sql = "Select document"
        sql += " From Document document"
        sql += " Where document.type = 'CHARGING'"
        return len(self._entityManager.createQuery(sql).getResultList())
    
    def getTemplateName(self):
        return "charging"
    