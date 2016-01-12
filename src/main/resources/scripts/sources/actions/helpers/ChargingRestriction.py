from actions.helpers.Restriction import Restriction
from entities.BookingPeriod import BookingPeriodManager

class ChargingRestriction(Restriction):
    
    def canProceed(self):
        activePossessions = self.countActivePossessions()
        createdChargings = self.countChargings()
        if activePossessions == createdChargings:
           return True
        else:
            self._message = "Brakuje %d naliczeń" % (createdChargings - activePossessions)
            return False
        
    def countActivePossessions(self):
        sql = "Select count(possession) From Possession possession Join possession.community community Where community.outDate is Null"
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def countChargings(self):
        currentMonth = BookingPeriodManager().getCurrentMonth()
        sql = "Select Distinct count(document)"
        sql += " From Document document Join document.positions position Join position.bookingPeriod bookingPeriod"
        sql += (" Where bookingPeriod.defaultPeriod = 1 and position.month = %d and document.type = 'CHARGING'" % currentMonth)
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def getTemplateName(self):
        return "charging"