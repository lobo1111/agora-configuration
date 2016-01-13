from actions.helpers.Restriction import Restriction
from entities.BookingPeriod import BookingPeriodManager

class ChargingRestriction(Restriction):
    
    def calculate(self):
        activePossessions = self.countActivePossessions()
        createdChargings = self.countChargings()
        if activePossessions == createdChargings:
           self._result = True
        else:
            self._loger.info("Found %d chargins but there are %d active possessions" % (createdChargings, activePossessions))
            self._message = "Brakuje %d naliczen" % (activePossessions - createdChargings)
            self._result = False
        
    def countActivePossessions(self):
        sql = "Select count(possession) From Possession possession Join possession.community community Where community.outDate is Null"
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def countChargings(self):
        currentMonth = BookingPeriodManager().getCurrentMonth()
        sql = "Select document.id, position.month"
        sql += " From Document document"
        sql += " Join document.positions position"
        sql += " Where document.type = 'CHARGING'"
        sql += " Group By document.id"
        sql += (" Having position.month = %s" % currentMonth)
        return len(self._entityManager.createQuery(sql).getResultList())
    
    def getTemplateName(self):
        return "charging"
    