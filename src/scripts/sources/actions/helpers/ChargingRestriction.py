from actions.helpers.Restriction import Restriction
from structures.BookingPeriod import BookingPeriodManager

class ChargingRestriction(Restriction):
    
    def calculate(self):
        missingChargings = self.countMissingChargings()
        return (missingChargings == 0)
        
    def countMissingChargings(self):
        sql = "SELECT count(possession) "
        sql += "FROM  "
        sql += "Possession possession "
        sql += "WHERE possession.id not in( "
        sql += "Select dp.document.possession.id "
        sql += "From DocumentPosition dp "
        sql += "Where dp.month in (select d.value From Dictionary d Where d.type.type = \"PERIODS\" and d.key = \"CURRENT\") "
        sql += "And dp.bookingPeriod.defaultPeriod = 1) "
        sql += "AND possession.community.inDate != NULL "
        sql += "AND possession.community.outDate = NULL "
        return self._entityManager.createQuery(sql).getSingleResult()